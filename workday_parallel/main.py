import json, multiprocessing , time, datetime
from data_extracter import jobdata_extracter
import numpy as np


urllist = []
queue = multiprocessing.Queue()
with open("robots.json","r") as f:
    jsonobjs = f.readlines()
    for jsonobj in jsonobjs:
        jsonobj = json.loads(jsonobj)
        for url in jsonobj['Sitemap']:
            urllist.append(url.rsplit("/", 1)[0])

np.random.shuffle(urllist)
# urllist = urllist[:24]

# parallel processing

def worker(urllist):
    results = []
    test = jobdata_extracter()
    try:
        for url in urllist:
            result = test.data_extracter(url)
            result = str(result).replace("'",'"')
            results.append(result)
            # if result is not list:
            #     with open('exceptions.json','a') as f:
            #         f.write(str(result) + '\n')
            # else:
            #     with open('jobdata.json','a') as f:
            #         f.write(str(result) + '\n')
    except KeyboardInterrupt:
        results.pop(-1)
        print("KeyboardInterrupt detected stopping the process")
    return results

def listener(queue):
    while 1:
        m = queue.get()
        print(m)

def main():
    processes = 8
    pool = multiprocessing.Pool(processes)
    result = pool.map_async(worker,np.array_split(urllist,processes))
    # queue.put(result)
    with open(f'workday_parallel/outputs/{datetime.datetime.today().date()}.json','a', encoding="utf-8") as f:
        try:
            for i in result.get():
                for jsonobj in i:
                    try :
                        data = json.loads(jsonobj)
                        if isinstance(data, list):
                            f.write(str(jsonobj) + '\n')
                        else:
                            with open('workday_parallel/outputs/exceptions.json','a') as exc:
                                exc.write(str(jsonobj) + '\n')
                    except json.decoder.JSONDecodeError:
                        with open('workday_parallel/outputs/exceptions.json','a') as exc:
                            exc.write(str(jsonobj) + 'json decode error detected'+ '\n')

        except KeyboardInterrupt:
            for i in result.get(15):
                for jsonobj in i:
                    try :
                        data = json.loads(jsonobj)
                        if isinstance(data, list):
                            f.write(str(jsonobj) + '\n')
                        else:
                            with open('exceptions.json','a') as exc:
                                exc.write(str(jsonobj) + '\n')
                    except json.decoder.JSONDecodeError:
                        with open('exceptions.json','a') as exc:
                            exc.write(str(jsonobj) + 'json decode error detected' + '\n' )
    pool.close()
    pool.join()
    

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))