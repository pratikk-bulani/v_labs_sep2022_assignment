import argparse, pandas as pd, fastwer

# Arguments passed at command line
parser = argparse.ArgumentParser()
parser.add_argument("--pred_path", type=str, default='./pred.xlsx', help="path to the pred.xlsx")
parser.add_argument("--gt_path", type=str, default='./gt.xlsx', help="path to the gt.xlsx")
parser.add_argument("--output_path", type=str, default='./output.xlsx', help="path to the output.xlsx")
args = parser.parse_args()

df_pred = pd.read_excel(args.pred_path)
df_gt = pd.read_excel(args.gt_path)
df_output = {} # Will store the output
df_pred['Id'] = df_pred['Id'].str.lower() # Lower case the Id column
df_gt['Id'] = df_gt['Id'].str.lower() # Lower case the Id column
df_join_gt_pred = pd.merge(df_pred, df_gt, on=['Id', 'Id']) # Join the data frames on Id column
nones = [None]*(df_gt.shape[0]-1)
del df_pred

df_cer_per_row = df_join_gt_pred.apply(lambda x: fastwer.score_sent(x.PRED, x.GT, char_level=True), axis=1)
df_wer_per_row = df_join_gt_pred.apply(lambda x: fastwer.score_sent(x.PRED, x.GT), axis=1)
df_output['CER per Row'] = list(df_cer_per_row.to_numpy())
df_output['WER per Row'] = list(df_wer_per_row.to_numpy())
df_output['CER corpus'] = [fastwer.score(df_join_gt_pred.PRED, df_join_gt_pred.GT, char_level=True), *nones]
df_output['WER corpus'] = [fastwer.score(df_join_gt_pred.PRED, df_join_gt_pred.GT), *nones]

df_characters_per_row = df_gt['GT'].apply(lambda row: len(row)) # Count the number of characters within each GT cell
df_output['Total Lines'] = [df_characters_per_row.shape[0], *nones]
df_output['Total Characters Per Row'] = list(df_characters_per_row.to_numpy())
df_output['Total Characters'] = [df_characters_per_row.to_numpy().sum(), *nones]

pd.DataFrame(df_output).to_excel(args.output_path)