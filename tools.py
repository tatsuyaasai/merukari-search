# tools
import datetime


def timeget(timestamp, from_when):
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    if from_when == "m":
        dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S').strftime('%m/%d')
        return dt
    elif from_when == "y":
        dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        return dt


if __name__ == "__main__":
    print(timeget(str(1653594470), "y"))
    print(timeget(str(1653594470), "m"))
