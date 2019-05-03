import functions as fn

# top10 = fn.top_10()
# print(top10[0])
# print('There were ' + str(top10[1]) + ' players that appeared in the top 10 of 2018 and 2019.')


import time
start = time.time()
fn.nationality_overall()
end = time.time()
print('time: ' + str(end - start))
