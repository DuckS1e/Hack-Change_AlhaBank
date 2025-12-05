# train_catboost_wmae_fixed_final.py
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error
from catboost import CatBoostRegressor, Pool

warnings.filterwarnings('ignore')
RND = 42

print("\n=== START: CatBoost WMAE pipeline ===\n")

# -------------------------
# 1. READ DATA
# -------------------------
TRAIN_FILE = "hackathon_income_train.csv"
TEST_FILE = "hackathon_income_test.csv"

train = pd.read_csv(TRAIN_FILE, sep=';', encoding='utf-8')
test = pd.read_csv(TEST_FILE, sep=';', encoding='utf-8')

print(f"Train shape: {train.shape}")
print(f"Test shape:  {test.shape}")

# -------------------------
# 2. FEATURE LIST
# -------------------------
selected_features = [
    'age', 'gender', 'region', 'adminarea', 'city_smart_name', 'nonresident_flag',
    'monthly_income', 'incomeValue', 'incomeValueCategory', 'salary_6to12m_avg',
    'dp_ils_avg_salary_1y', 'dp_ils_avg_salary_2y', 'dp_ils_avg_salary_3y',
    'active_loans_count', 'loan_cnt', 'pil', 'other_credits_count',
    'bki_total_products', 'hdb_bki_total_active_products', 'hdb_bki_total_cnt',
    'hdb_bki_last_product_days', 'hdb_bki_total_max_limit',
    'hdb_bki_total_pil_max_limit', 'hdb_bki_total_cc_max_limit',
    'hdb_bki_total_ip_max_limit', 'hdb_bki_total_auto_max_limit',
    'hdb_bki_total_max_overdue_sum', 'ovrd_sum', 'total_sum',
    'turn_cur_cr_avg_v2', 'turn_cur_cr_sum_v2', 'turn_cur_cr_max_v2',
    'turn_cur_cr_min_v2', 'avg_credit_turn_rur', 'diff_avg_cr_db_turn',
    'turn_cur_db_avg_v2', 'turn_cur_db_sum_v2', 'turn_cur_db_max_v2',
    'avg_debet_turn_rur', 'avg_cur_db_turn',
    'curr_rur_amt_cm_avg', 'curr_rur_amt_3m_avg', 'min_balance_rur_amt_6m_af',
    'max_balance_rur_amt_1m_af', 'total_rur_amt_cm_avg',
    'dda_rur_amt_curr_v2', 'dda_rur_amt_3m_avg', 'loanacc_rur_amt_curr_v2',
    'transaction_category_supermarket_percent_cnt_2m',
    'transaction_category_supermarket_sum_cnt_m2',
    'transaction_category_restaurants_percent_cnt_2m',
    'transaction_category_fastfood_percent_cnt_2m',
    'transaction_category_cash_percent_amt_2m',
    'avg_amount_daily_transactions_90d',
    'by_category__amount__sum__eoperation_type_name__ishodjaschij_bystryj_platezh_sbp',
    'by_category__amount__sum__eoperation_type_name__vhodjaschij_bystryj_platezh_sbp',
    'by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona',
    'by_category__amount__sum__eoperation_type_name__perevod_s_karty_na_karty',
    'avg_by_category__amount__sum__cashflowcategory_name__supermarkety',
    'avg_by_category__amount__sum__cashflowcategory_name__kafe',
    'avg_by_category__amount__sum__cashflowcategory_name__produkty',
    'avg_by_category__amount__sum__cashflowcategory_name__odezhda',
    'client_active_flag', 'days_to_last_transaction', 'mob_cnt_days',
    'mob_total_sessions', 'device_iphone_avg',
    'dp_address_unique_regions', 'tz_msk_timedelta', 'blacklist_flag',
    'profit_income_out_rur_amt_12m', 'profit_income_out_rur_amt_9m',
    'loan_cur_amt', 'first_salary_income', 'label_Above_1M_share_r1',
    'label_Below_50k_share_r1'
]

features = [f for f in selected_features if f in train.columns and f in test.columns]
print(f"Используемые признаки: {len(features)}")


# -------------------------
# 3. CLEAN / PARSE STRINGS (FIXED)
# -------------------------
def smart_convert_fixed(df, df_test):
    df = df.copy()
    df_test = df_test.copy()

    for c in df.columns:
        if df[c].dtype == 'object':
            s = df[c].astype(str).str.replace(',', '.', regex=False)
            numeric = pd.to_numeric(s, errors='coerce')
            if numeric.notna().mean() > 0.5:
                # Числовая колонка
                med = numeric.median()
                df[c] = numeric.fillna(med)
                if c in df_test.columns:
                    df_test[c] = pd.to_numeric(df_test[c].astype(str).str.replace(',', '.', regex=False),
                                               errors='coerce').fillna(med)
            else:
                # Категориальная колонка
                df[c] = s.replace({'nan': '__NA__', '': '__NA__'})
                if c in df_test.columns:
                    df_test[c] = df_test[c].astype(str).replace({'nan': '__NA__', '': '__NA__'})
    return df, df_test


train, test = smart_convert_fixed(train, test)

# -------------------------
# 4. Prepare X, y, weights
# -------------------------
TARGET = 'target'
WEIGHT = 'w'
ID = 'id'

y = train[TARGET].copy()
if WEIGHT in train.columns:
    weights = pd.to_numeric(train[WEIGHT], errors='coerce').fillna(1.0)
else:
    weights = pd.Series(np.ones(len(train)), index=train.index)

X = train[features].copy()
X_test = test[features].copy()

num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
cat_candidates = [c for c in features if c not in num_cols]

# Заполняем NaN медианой для числовых
for c in num_cols:
    med = X[c].median()
    X[c] = X[c].fillna(med)
    if c in X_test.columns:
        X_test[c] = X_test[c].fillna(med)

# Категориальные в str
for c in cat_candidates:
    X[c] = X[c].astype(str)
    if c in X_test.columns:
        X_test[c] = X_test[c].astype(str)

cat_features = [c for c in X.columns if X[c].dtype == 'object']
print(f"Категориальных признаков: {len(cat_features)}")


# -------------------------
# 5. MODELING: CatBoost CV
# -------------------------
def wmae(y_true, y_pred, w):
    return np.sum(w * np.abs(y_true - y_pred)) / np.sum(w)


N_SPLITS = 5
kf = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RND)

oof_preds = np.zeros(len(X))
test_preds = np.zeros(len(X_test))

fold = 0
for tr_idx, val_idx in kf.split(X, y):
    fold += 1
    print(f"\n--- Fold {fold}/{N_SPLITS} ---")
    X_tr, X_val = X.iloc[tr_idx], X.iloc[val_idx]
    y_tr, y_val = y.iloc[tr_idx], y.iloc[val_idx]
    w_tr, w_val = weights.iloc[tr_idx], weights.iloc[val_idx]

    train_pool = Pool(X_tr, label=y_tr, weight=w_tr, cat_features=cat_features)
    val_pool = Pool(X_val, label=y_val, weight=w_val, cat_features=cat_features)
    test_pool = Pool(X_test, cat_features=cat_features)

    model = CatBoostRegressor(
        iterations=5000,
        learning_rate=0.03,
        depth=6,
        l2_leaf_reg=5,
        loss_function='MAE',
        eval_metric='MAE',
        random_seed=RND,
        early_stopping_rounds=200,
        task_type='CPU',
        verbose=200
    )

    model.fit(train_pool, eval_set=val_pool, use_best_model=True)

    oof_preds[val_idx] = model.predict(X_val)
    test_preds += model.predict(X_test) / N_SPLITS

    fold_mae = mean_absolute_error(y_val, oof_preds[val_idx])
    fold_wmae = wmae(y_val.values, oof_preds[val_idx], w_val.values)
    print(f"Fold {fold} MAE: {fold_mae:.2f}, WMAE: {fold_wmae:.2f}")

# -------------------------
# 6. FINAL METRICS & SAVE
# -------------------------
oof_mae = mean_absolute_error(y, oof_preds)
oof_wmae = wmae(y.values, oof_preds, weights.values)
print("\n=== OOF RESULTS ===")
print(f"OOF MAE : {oof_mae:.2f}")
print(f"OOF WMAE: {oof_wmae:.2f}")

# -------------------------
# 7. Save submission
# -------------------------
sub = pd.DataFrame({
    'id': test[ID] if ID in test.columns else np.arange(len(test)),
    'target': test_preds
})
sub['target'] = sub['target'].clip(lower=0)
sub.to_csv('submission_catboost.csv', index=False)
print("Submission saved -> submission_catboost.csv")
