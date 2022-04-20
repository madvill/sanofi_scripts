import sys
import pandas as pd
from ..utils import get_logger, set_log_level
from datetime import datetime, timedelta

# Init logger
logger = get_logger('unpivot')
set_log_level(logger, "info")

def unpivot_file(file, country):
    # Read excel file
    df = pd.read_excel(file)

    logger.info("File read successful")

    if country == "MX":

        # Make groups over column names (Un, Lc and others)
        col_un = []
        col_lc = []
        other_col = []
        for i in df.columns:
            if "Un " in i:
                col_un.append(i)
            elif "Lc " in i:
                col_lc.append(i)
            else:
                other_col.append(i)

        logger.info("Start WeekOfYear treatment")
        # Changing column name of date columns in YYYY_WW format
        df.rename(
            inplace=True,
            columns=lambda x: str(x)[12:] + "_" + str(x)[9:11] if x in col_un else x,
        )

        col_un = [a[12:] + "_" + a[9:11] for a in col_un]

        logger.info("Start meltings")
        # Create temporary dataframes with unpivoted Un and Lc
        tmp_df1 = pd.melt(
            df,
            id_vars=other_col,
            value_vars=col_un,
            var_name="WeekOfYear",
            value_name="Unit",
        )
        tmp_df2 = pd.melt(
            df,
            id_vars=other_col,
            value_vars=col_lc,
            var_name="WeekOfYear",
            value_name="Value",
        )

        logger.info("Start concat")
        # Concatenate the temporary dataframes to get the unpivot on only one dataframe
        new_df = pd.concat([tmp_df1, tmp_df2["Value"]], axis=1, join="inner")
    elif country == "JP":
        col_date = []
        other_col = []
        for i in df.columns:
            if "/" in i:
                col_date.append(i)
            else:
                other_col.append(i)

        logger.info("Start WeekOfYear treatment")
        # Changing column name of date columns in YYYY_WW format

        df.rename(
            inplace=True,
            columns=lambda x: str(x).replace("-", "") if x in col_date else x,
        )

        col_date = [str(x).replace("-", "") for x in col_date]

        df.rename(
            inplace=True,
            columns=lambda x: str(x)[0:5] + "0" + str(x)[5:]
            if len(x) == 6 and x in col_date
            else x,
        )

        col_date = [
            str(x)[0:5] + "0" + str(x)[5:] if len(x) == 6 else str(x) for x in col_date
        ]

        logger.info("Start melting")
        # Create the new dataframe with unpivoted date columns
        new_df = pd.melt(
            df,
            id_vars=other_col,
            value_vars=col_date,
            var_name="YearMonth",
            value_name="Value",
        )
    elif country == "JP2":
        col_date = []
        other_col = []
        for i in df.columns:
            if "." in i:
                col_date.append(i)
            else:
                other_col.append(i)

        logger.info("Start date treatment")

        start_year = file.split("/")[-1].split("_")[4][:4]
        dt_col_count = len(col_date)
        col_date_ = [dt.replace("-", "").replace(".", "-") for dt in col_date]
        first_date = start_year + "-" + col_date_[0]
        first_date = datetime.strptime(first_date, "%Y-%m-%d")
        date_list = [first_date.strftime("%Y-%m-%d")]
        delta = timedelta(days=7)
        for i in range(dt_col_count - 1):
            date = first_date + delta
            first_date = date
            date_list.append(date.strftime("%Y-%m-%d"))

        df.columns = other_col + date_list

        logger.info("Starting melting")

        new_df = pd.melt(
            df,
            id_vars=other_col,
            value_vars=date_list,
            var_name="Date",
            value_name="Value",
        )

    logger.info("Start writing in csv")
    # Write the unpivoted dataframe in csv in the same directory as the initial file
    new_df.to_csv(file.split(".")[0] + "_pivoted.csv", index=False, sep="|")
