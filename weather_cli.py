from argparse import ArgumentParser
from datetime import date
from logging import basicConfig, info

import pandas as pd
from matplotlib import pyplot as plt

# ------------------------------------------------------------------------------------
# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------------

basicConfig(
    filename="files/log/test.log",
    level=20,
    format="%(asctime)s:%(levelname)s:%(name)s:line#:%(lineno)s:%(message)s",
    filemode="w",
    datefmt="%d-%b-%y %H:%M:%S",
)


# data=pd.DataFrame()     #for using imported data in next CLI
# result=list()


# ------------------------------------------------------------------------------------
# CMD-1     IMPORT
# ------------------------------------------------------------------------------------


def import_dataset(file_name):
    # global data
    df = pd.DataFrame()
    if file_name.endswith(".csv"):
        try:
            df = pd.read_csv(f"files/dataset/{file_name}")
            info(f"dataset from {file_name} is imported")
            print(f"{file_name} is imported")
            # print(df.head)
            data = df
            print(data.head())
            return True
        except NameError:
            print(f"File:{file_name} not found")
            return False

    elif file_name.endswith(".txt"):
        try:
            df = pd.read_csv(file_name, sep=" ")
            info(f"dataset from {file_name} is imported")
            print(f"{file_name} is a text file, imported")
            return True
        except NameError:
            print(f"File:{file_name} not found")
    else:
        print(f"{file_name} is not in valid format")
        return False
    return False


# ------------------------------------------------------------------------------------
# CMD-2     ANALYZE DATASET
# ------------------------------------------------------------------------------------


def analyze_dataset(range):
    try:
        d = pd.read_csv("files/dataset/weather.csv")
        info("Dataset from weather.csv is imported")
    except NameError:
        print("File not found")
        return
    if range:
        range = range.split(" ")
        start = range[0]
        sy, sm, sd = [int(x) for x in start.split("-")]

        end = range[2]
        ey, em, ed = [int(x) for x in end.split("-")]

        d1 = date(sy, sm, sd)
        d2 = date(ey, em, ed)

        if d1 < d2:
            try:
                new_df = d[
                    (d["Day"] >= sd)
                    & (d["Month"] >= sm)
                    & (d["Year"] >= sy)
                    & (d["Day"] <= ed)
                    & (d["Month"] <= em)
                    & (d["Year"] <= ey)
                ]

            except ValueError:
                print(
                    "Invalid Range, \
                     Format'Starting Date to Ending Date'"
                )
                return
        try:
            print(new_df.head())
            print(new_df.shape)
        except ValueError:
            print("Data not found")
            return
        avg_temp = int()
        min_temp = int()
        max_temp = int()
        windiest = str()
        info("Perfoming analytics on dataset")
        avg_temp = new_df["Avg Temp"].mean()
        min_temp = new_df["Min Temp"].min()
        max_temp = new_df["Max Temp"].max()
        windspeed = new_df["Wind.Speed"].max()
        windiest = new_df["Wind.Speed"].idxmax()
        windiest_day = new_df.loc[windiest, "Date.Full"]

        print(
            f"Average temp from {sd}/{sm}/{sy} \
            to {ed}/{em}/{ey} : {avg_temp}"
        )
        print(
            f"Minimum temp from {sd}/{sm}/{sy} \
            to {ed}/{em}/{ey} : {min_temp}"
        )
        print(
            f"Maximum temp from {sd}/{sm}/{sy} \
            to {ed}/{em}/{ey} : {max_temp}"
        )
        print(
            f"Windiest Day between {sd}/{sm}/{sy} \
                to {ed}/{em}/{ey} : {windiest_day} speed({windspeed})"
        )

        d["Date.Full"] = pd.to_datetime(d["Date.Full"])
        mask = (d["Date.Full"] >= start) & (d["Date.Full"] <= end)

        df_range = d.loc[mask]
        plt.plot(df_range["Date.Full"], df_range["Avg Temp"])
        plt.title("Humidity Trend")
        plt.xlabel("Date")
        plt.ylabel("Humidity")
        plt.show()
        val_list = [avg_temp, min_temp, max_temp]

        x = pd.DataFrame(
            [[avg_temp, min_temp, max_temp]],
            columns=["avg_temp", "min_temp", "max_temp"],
        )
        path = "files/result/"
        x.to_csv(path + "results.csv", index=False)
        info("Results exported")
        return val_list
    else:
        print("range not defined")

    return val_list


# ------------------------------------------------------------------------------------
# CMD-3     EXPORT
# ------------------------------------------------------------------------------------


def export_results(format):
    if format == "csv":
        print("results are exported")
        return True
        # x=pd.DataFrame([[res[0]],[res[1]],[res[2]]]
        #                ,columns=['avg_temp','min_temp','max_temp'])
        # x.to_csv('results.csv',index=False)


# ------------------------------------------------------------------------------------
# INITIATING CLIs
# ------------------------------------------------------------------------------------


def initiate_cli():
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="cmd")

    parser_cmd1 = sub_parser.add_parser("import", help="imports the file")
    parser_cmd1.add_argument("-f", "--file", help="stores filename", type=str)

    parser_cmd2 = sub_parser.add_parser(
        "analyze",
        help="for performing analytics",
    )
    parser_cmd2.add_argument("-r", "--range", help="stores range", type=str)

    parser_cmd3 = sub_parser.add_parser(
        "export",
        help="for exporting analytics in a file",
    )
    parser_cmd3.add_argument(
        "-fr",
        "--format",
        help="specifies format",
        type=str,
        choices=["csv", "txt"],
    )

    args = parser.parse_args()

    if args.cmd == "import":
        import_dataset(args.file)

    elif args.cmd == "analyze":
        try:
            analyze_dataset(args.range)
        except ValueError:
            print("'YYYY/MM/DD to YYYY/MM/DD' this is format for range string")

    elif args.cmd == "export":
        export_results(args.format)

    else:
        print("invalid cmd")


# ------------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    initiate_cli()
