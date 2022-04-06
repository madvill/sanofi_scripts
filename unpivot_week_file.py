from ntpath import join
import os
import sys
import pandas as pd
"""
dir = str(input("Where is the directory ?"))
file = str(input("What's the name of the xlsx file ?"))
#dir='/content/'
#file = 'IQVIA_Weekly_SO_MX_202212.xlsx'
"""
from pickle import FALSE
import argparse
from utils import set_log_level, get_logger

# Init logger
logger = get_logger(sys.argv[0])


def main():
    parser = argparse.ArgumentParser(description='lol')
    parser.add_argument('--file', help="Input file path", required=True)
    parser.add_argument('--verbose', help="Debug mode", required=False, default=False)


    args = parser.parse_args()

    file = args.file

    if args.verbose:
        set_log_level(logger,"debug")
        logger.debug(f"Command line arguments: {args}")
    
    df = pd.read_excel(file)

    logger.info('File read successful')

    col_un = []
    col_lc = []
    other_col = []
    for i in df.columns:
      if 'Un ' in i :
        col_un.append(i)
      elif 'Lc ' in i :
        col_lc.append(i)
      else :
        other_col.append(i)
    
    logger.info('Start WeekOfYear treatment')
    df.rename(inplace=True,columns=lambda x: str(x)[12:]+'_'+str(x)[9:11] if x in col_un else x)

    col_un = [a[12:]+'_'+a[9:11] for a in col_un]
    #tmp_df = pd.melt(df, id_vars=other_col+col_lc, value_vars=col_un, var_name='WeekOfYear', value_name='Unit')

    #new_df = pd.melt(tmp_df, id_vars=other_col+['WeekOfYear','Unit'], value_vars=col_lc, var_name='WeekOfYear1', value_name='Value').fillna(0)

    logger.info('Start meltings')

    tmp_df1 = pd.melt(df, id_vars=other_col, value_vars=col_un, var_name='WeekOfYear', value_name='Unit')
    tmp_df2 = pd.melt(df, id_vars=other_col, value_vars=col_lc, var_name='WeekOfYear', value_name='Value')

    logger.info('Start concat')

    new_df = pd.concat([tmp_df1,tmp_df2['Value']],axis=1,join='inner')

    #del new_df['WeekOfYear1']
    #logger.info('Start WeekOfYear treatment')
    #new_df['WeekOfYear'] = [a[12:]+'_'+a[9:11] for a in new_df['WeekOfYear']]

    logger.info('Start writing in csv')
    new_df.to_csv(file[:-5]+'_pivoted.csv',index=False)


if __name__ == "__main__":
    set_log_level(logger,"info") 
    main()

