from datetime import *

def calculate_weekenddays_between(datetime1, datetime2):
    """
        Returns the number of weekend days between the 2 dates passed as parameters.
        The result is returned in form of a positive timedelta object. This means that
        it doesn't matter the order of the datetimes given as parameters.
    """
    if datetime1==datetime2:
        return timedelta(0)
    ## The dates are ordered so d1 < d2
    if datetime1 < datetime2:
        d1 = datetime1
        d2 = datetime2
    else:
        d1 = datetime2
        d2 = datetime1

	## monday1 = the monday after d1
    monday1 = (d1 + timedelta(8 - d1.isoweekday())).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    ## monday2 = the monday before d2
    monday2 = (d2 - timedelta( d2.isoweekday() - 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    ## if monday1 <= monday2 => the dates are not in the same week
    if monday1 <= monday2:
        dif1 = monday1 - d1
        if dif1.days > 2:
            dif1 = timedelta(2)
        dif2 = d2 - monday2
        if dif2.days <= 5:
            dif2 = timedelta()
        else:
            dif2 = dif2 - timedelta(5)
        return dif1 + dif2 + (monday2 - monday1) / 7 * 2
    ## the dates are in the same week
    else:
        ## both dates are working days
        if d2.isoweekday() <= 5:
            return timedelta()
        ## both dates are weekend days
        elif d1.isoweekday() > 5:
            return d2 - d1
        else:
            return d2 - monday2 - timedelta(5)

def calculate_workingdays_between(datetime1, datetime2):
    """
        Returns the number of workingdays days between the 2 dates passed as parameters.
        The result is returned in form of a positive timedelta object. This means that
        it doesn't matter the order of the datetimes given as parameters.
    """
    if datetime1==datetime2:
        return timedelta(0)
    ## The dates are ordered so d1 < d2
    if datetime1 < datetime2:
        d1 = datetime1
        d2 = datetime2
    else:
        d1 = datetime2
        d2 = datetime1
    return d2 - d1 - calculate_weekenddays_between(d1, d2)

def main():
    """
    Testing the functions
    """
    ## 2 dates in the same week
    dt1 = datetime(2006, 11, 29)    # working day
    dt2 = datetime(2006, 11, 27)    # working day
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    dt1 = datetime(2006, 11, 29)    # working day
    dt2 = datetime(2006, 12, 2)     # saturday
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    dt1 = datetime(2006, 11, 3)    # sunday
    dt2 = datetime(2006, 12, 2)    # saturday
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    ## 2 dates in consecutive weeks
    dt1 = datetime(2006, 11, 29)    # working day
    dt2 = datetime(2006, 12, 5)     # working day
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    dt1 = datetime(2006, 11, 29)    # working day
    dt2 = datetime(2006, 12, 10)     # working day
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    ## 2 dates in different weeks
    dt1 = datetime(2006, 11, 26)    # sunday
    dt2 = datetime(2006, 12, 5)     # working day
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

    dt1 = datetime(2006, 11, 24)    # working day
    dt2 = datetime(2006, 12, 6)     # working day
    print dt1
    print dt2
    print "weekenddays: " + str(calculate_weekenddays_between(dt1, dt2))
    print "workingdays: " + str(calculate_workingdays_between(dt1, dt2))

if __name__ == "__main__":
    main()