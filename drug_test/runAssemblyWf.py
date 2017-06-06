
import sys
import os
import time
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.histories import HistoryClient
from bioblend.galaxy.tools import ToolClient
from bioblend.galaxy.workflows import WorkflowClient
from bioblend.galaxy.datasets import DatasetClient


GALAXY_URL = 'https://genomics.tbportal.org/galaxy/'
API_KEY = '5cb1e5bb92e2b6aea15dd605431b362e'
WORKFLOW_ID = '33b43b4e7093c91f'
TOOL_ID_IN_GALAXY = 'toolshed.g2.bx.psu.edu/repos/mandorodriguez/fastqdump_paired/fastq_dump_paired/1.1.4'


def findDatasedIdByExtention(datasetClient, output, ext):
    id = ''
    for datasetId in output['outputs']:
        dataset = datasetClient.show_dataset(datasetId)
        if dataset['file_ext'] == ext:
            id = datasetId
            break
    return id



def downloadDataset(datasetClient, datasetId, outpath):
    if datasetId != '':
        datasetClient.download_dataset(datasetId, outpath, False, True)
    else:
        print 'Dataset id %s not found. Fail to download dataset to % s.' % (datasetId, outpath)



def purge_dataset(histClient, history_id, dataset_id, purge=False):

    url = histClient.gi._make_url(histClient, history_id, contents=True)

    # Append the dataset_id to the base history contents URL
    url = '/'.join([url, dataset_id])
    payload = {}
    if purge is True:
        payload['purge'] = purge

    histClient._delete(payload=payload, url=url)

############


galaxyInstance = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

historyClient = HistoryClient(galaxyInstance)
toolClient = ToolClient(galaxyInstance)
workflowClient = WorkflowClient(galaxyInstance)
datasetClient = DatasetClient(galaxyInstance)


# Set SRR name for history and for workflow input

with open('IDfile.txt') as f:
    SRR_list = f.read().splitlines()


###########################################
# Let's use multithreading functionality to start workflows

from multiprocessing.dummy import Pool as ThreadPool

def run_workflow(input_srr):
    history = historyClient.create_history(input_srr)
    workflow = workflowClient.show_workflow(WORKFLOW_ID)
    dataset_map = {workflow['inputs'].keys()[0]: {'id': 'b5a63c4aad3b8943', 'src': 'hda'}}
    params = {TOOL_ID_IN_GALAXY: {'param': 'accession_number', 'value': input_srr}}

    output = workflowClient.invoke_workflow(WORKFLOW_ID, dataset_map, params, history['id'])

    print ('WR launched')
    print (output)

    history_id = output['history_id']

    print ('history id = ', history_id)

    # give the workflow some time to update history and create dataset records
    time.sleep(10)


    show_history = historyClient.show_history(history_id, contents=True)

    print ('show history')
    print (show_history)

    final_dataset_id = show_history[-1]['dataset_id']

    print ('final dataset')
    print (final_dataset_id)


    if final_dataset_id != '':
        datasetClient.download_dataset(final_dataset_id, file_path='VCFs/' + input_srr + '.vcf',
                                       use_default_filename=False, wait_for_completion=True)
        print ('vcf downloaded')
    else:
        print 'Dataset id not found. Fail to download dataset to'


    all_datasets = [show_history[i]['dataset_id'] for i in range(len(show_history))]

    print ('dataset extracted')
    for dataset_id in all_datasets[:-1]:
        historyClient.delete_dataset(history_id, dataset_id)
        purge_dataset(historyClient, history_id, dataset_id, purge=True)

        print (dataset_id, 'deleted')

    print (input_srr, 'finished!')


pool = ThreadPool()

results = pool.map(run_workflow, SRR_list[7:8])

pool.close()

# wait until all threads finish
pool.join()



