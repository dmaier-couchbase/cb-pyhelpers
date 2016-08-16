## Creates one key per vBucket and upserts it to the bucket given bucket
# This can be checked by executing the following command on each node:
# /opt/couchbase/bin/couch_dbinfo *.couch.1 | grep 'doc count: 1' | wc -l

import zlib
from couchbase.bucket import Bucket

NUM_SAMPLES=10000
CON_STR='couchbase://192.168.7.141/default'

vBuckets = {}

for i in range(0,NUM_SAMPLES):
  key = 'repl_marker::' + str(i)
  crc = zlib.crc32(key)
  cb_crc = ((crc >> 16) & 0x7fff) &1023
  vBuckets[cb_crc]=key
  
print "Generated #keys:" + str(len(vBuckets))

if len(vBuckets) == 1024:
  for i in vBuckets.keys():
     key = vBuckets[i]
     print 'vB_' + str(i) + ':' + key

     c = Bucket(CON_STR)
     c.upsert(key, 'Replication Marker')
else:
     print 'Error: Not enough sample keys'

