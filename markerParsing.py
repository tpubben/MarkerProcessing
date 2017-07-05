import os, random, math

# open marker file and save to a new csv file with only point markers and their coordinates in UTM NAD83
# eastin, northing, elevation in meters

def calc_strikedip(ptA, ptB, ptC):

    x1, y1, z1 = float(ptA[0]), float(ptA[1]), float(ptA[2])
    x2, y2, z2 = float(ptB[0]), float(ptB[1]), float(ptB[2])
    x3, y3, z3 = float(ptC[0]), float(ptC[1]), float(ptC[2])


    u1 = float(((y1 - y2) * (z3 - z2) - (y3 - y2) * (z1 - z2)))
    u2 = float((-((x1 - x2) * (z3 - z2) - (x3 - x2) * (z1 - z2))))
    u3 = float(((x1 - x2) * (y3 - y2) - (x3 - x2) * (y1 - y2)))

    # calculate pseudo eastings and northings from origin
    if u3 < 0:
        easting = u2
    else:
        easting = -u2

    if u3 > 0:
        northing = u1
    else:
        northing = -u1
    # determine strike

    if easting >= 0:
        part2_strike = math.pow(easting, 2) + math.pow(northing, 2)
        strike = math.degrees(math.acos(northing / math.sqrt(part2_strike)))
    else:
        partB_strike = northing / math.sqrt(math.pow(easting, 2) + math.pow(northing, 2))
        strike = math.degrees(2 * math.pi - math.acos(partB_strike))

    # determine dip
    print(strike, 'strike')
    part1_dip = math.sqrt(math.pow(u2, 2) + math.pow(u1, 2))
    part2_dip = math.sqrt(math.pow(u1,2) + math.pow(u2,2) + math.pow(u3,2))
    dip = math.degrees(math.asin(part1_dip / part2_dip))

    return strike, dip

while True:
    f = open(input('Please enter full path to marker export file: '))
    working_dir = input('Please enter working directory: ')
    fo_name = os.path.join(working_dir,'tempFile.csv')
    try:
        os.remove(fo_name)
    except:
        pass
    result_file = os.path.join(working_dir, input('Please enter the name of the desired result file: '))
    if os.path.isfile(result_file):
        ovr_write_results = input('The results file exists, would you like to overwrite it? (y/n)')
        if ovr_write_results == 'y':
            os.remove(result_file)
        else:
            result_file = os.path.join(working_dir, input('Please enter a new name for the desired result file: '))

    with open(os.path.join(working_dir, fo_name), 'a') as outputfile:
        for line in f:
            if not line.startswith('#'):
                if line.startswith('p'):
                    fline = line.rstrip().split(',')
                    tempList = []
                    for item in fline:
                        if not item == '':
                            tempList.append(item)
                    newline = ''
                    x = 1
                    for item in tempList:
                        if x < 4:
                            newline = newline + item + ', '
                            x += 1
                        elif x == 4:
                            newline = newline + item + '\n'

                    with open(os.path.join(working_dir,fo_name), 'a') as outputfile:
                        outputfile.write(newline)



    # open up temp file to read the lines, strip off carriage returns and append to a list
    with open(os.path.join(working_dir, fo_name), 'r') as source:
        lines = [line.strip() for line in source]
        line_count = len(lines)

    if line_count > 3:
        # select 3 points at random from output file repeatedly to find average of many possible combinations

        iter_num = int(line_count * 9) # find the max number of times the sample points can be divided by 3 then add 2 extra
        x = 0
        strike_list = []
        dip_list = []
        while x <= iter_num:
            random_choice = random.sample(lines, 3)
            ptA = random_choice[0].split(',')[1:]
            ptB = random_choice[1].split(',')[1:]
            ptC = random_choice[2].split(',')[1:]
            temp_strike = calc_strikedip(ptA, ptB, ptC)[0]
            strike_list.append(temp_strike)
            temp_dip = calc_strikedip(ptA, ptB, ptC)[1]
            dip_list.append(temp_dip)
            result_line = str(temp_strike)+',strike,'+str(temp_dip)+',dip\n'
            with open(result_file, 'a') as export:
                export.write(result_line)
            x += 1

        print(strike_list)
        avg_strike = sum(strike_list) / float(len(strike_list))
        avg_dip = sum(dip_list) / float(len(dip_list))
        results_line = '\n'+str(avg_strike)+',average strike,'+str(avg_dip)+',average dip'
        with open(result_file, 'a') as results:
            results.write(results_line)

        print('Average strike:', avg_strike, 'degrees /', 'Average dip:', avg_dip, 'degrees')

    elif line_count == 3:

        ptA = lines[0].split(',')[1:]
        ptB = lines[1].split(',')[1:]
        ptC = lines[2].split(',')[1:]

        #with open(result_file, 'a') as export:
            #export.write('Average strike:', avg_strike, 'degrees /', 'Average dip:', avg_dip, 'degrees')
        results = calc_strikedip(ptA, ptB, ptC)
        print(results)
        result_line = str(results[0])+',strike,'+str(results[1])+',dip'
        with open(result_file, 'a') as result:
            result.write(result_line)

    else:
        print("There are not enough points in the file to calculate a surface.")
    f.close()
    os.remove(fo_name)
    break




