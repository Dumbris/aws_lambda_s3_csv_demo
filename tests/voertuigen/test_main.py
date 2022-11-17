import unittest
from unittest import mock
import io
import pandas as pd

# Setting the default AWS region environment variable required by the Python SDK boto3
with mock.patch.dict('os.environ', {'AWS_REGION': 'us-east-1'}):
    from voertuigen.main import lambda_handler

def mocked_read_csv_invalid(s3_client, bucket_name, key_name):
    return io.StringIO("")

def mocked_read_csv(s3_client, bucket_name, key_name):
    return io.StringIO("""Kenteken,Voertuigsoort,Merk,Handelsbenaming,Datum tenaamstelling,Inrichting,Aantal zitplaatsen,Eerste kleur,Aantal cilinders,Cilinderinhoud,Europese voertuigcategorie
45GBX1,Personenauto,OPEL,ASTRA GTC,20190308,coupe,5,ZWART,4,"1,796",M1
96XPG9,Personenauto,SUZUKI,SPLASH,20220222,stationwagen,5,BLAUW,3,996,M1
V243FN,Bedrijfsauto,VOLKSWAGEN,TRANSPORTER,20170323,open laadvloer,3,N.v.t.,4,"1,968",N1
VJ309T,Bedrijfsauto,VOLKSWAGEN,CADDY,20220525,gesloten opbouw,2,N.v.t.,4,"1,598",N1
JV401K,Personenauto,RENAULT,TWINGO,20201120,hatchback,4,ZWART,3,999,M1
61THKT,Personenauto,CITROEN,CITROEN C1,20220709,hatchback,4,ZWART,3,998,M1
98PJD2,Personenauto,PEUGEOT,206+,20150604,hatchback,5,GRIJS,4,"1,360",M1
SPGR69,Personenauto,VOLKSWAGEN,POLO 44 KW,20170505,hatchback,,WIT,4,"1,390",M1
12RDK9,Personenauto,RENAULT,MEGANE,20150226,stationwagen,5,GRIJS,4,"1,461",M1
32LJRF,Personenauto,FORD,FOCUS,20220218,hatchback,5,ZWART,4,"1,388",M1
VB784V,Bedrijfsauto,RENAULT,KANGOO,20220707,gesloten opbouw,2,N.v.t.,4,"1,461",N1
39TKHS,Personenauto,FIAT,FIAT PANDA,20210217,hatchback,4,ZWART,4,"1,242",M1
31TJT8,Personenauto,SUZUKI,SWIFT,20201204,hatchback,5,ZWART,4,"1,242",M1
2KXX98,Personenauto,MINI,MINI,20180203,hatchback,4,WIT,4,"1,598",M1
1SPH48,Personenauto,FORD,FIESTA,20131116,hatchback,5,GRIJS,4,"1,242",M1
03PPD8,Personenauto,MITSUBISHI,MITSUBISHI ASX,20110304,stationwagen,5,GRIJS,4,"1,590",M1
SG772P,Personenauto,SKODA,KODIAQ,20180407,stationwagen,5,GROEN,4,"1,395",M1
GH119B,Personenauto,VOLKSWAGEN,UP,20151102,hatchback,4,ROOD,3,999,M1
VS354L,Bedrijfsauto,VOLKSWAGEN,CRAFTER,20210210,gesloten opbouw,3,N.v.t.,4,"1,968",N1""")

def mocked_save(csv_buffer, s3_client, bucket, key):
    return

class CVSFileTest(unittest.TestCase):

    @mock.patch('voertuigen.main.read_file_s3', side_effect=mocked_read_csv)
    @mock.patch('voertuigen.main.save_to_s3', side_effect=mocked_save)
    def test_valid_file(self, save_file_mock, read_file_mock):

        response = lambda_handler(self.s3_upload_event("data.csv"), "")
        expected_response = True        
        self.assertEqual(read_file_mock.call_count, 1)

        #TODO: check output content
        #name, args, kwargs = save_file_mock.mock_calls[0]
        #self.assertEquals(args, ())
        #self.assertEquals(kwargs, {})

        self.assertEqual(save_file_mock.call_count, 17)
        self.assertEqual(response, expected_response)
    
    # Test for invalid file type (.txt)
    @mock.patch('voertuigen.main.read_file_s3', side_effect=mocked_read_csv_invalid)
    def test_invalid_file(self, read_file_mock):

        with self.assertRaises(pd.errors.EmptyDataError):
            response = lambda_handler(self.s3_upload_event("invalid_file.txt"), "")
        self.assertEqual(read_file_mock.call_count, 1)

    # Mock S3 new file uploaded event
    def s3_upload_event(self, file_name):
        return {
            "Records":[
            {
                "eventVersion":"2.1",
                "eventSource":"aws:s3",
                "awsRegion":"us-east-1",
                "eventTime":"2021-06-18T16:03:17.567Z",
                "eventName":"ObjectCreated:Put",
                "userIdentity":{
                    "principalId":"AWS:AIDAI7123123XY"
                },
                "requestParameters":{
                    "sourceIPAddress":"12.21.123.69"
                },
                "responseElements":{
                    "x-amz-request-id":"D104123123BXXE",
                    "x-amz-id-2":"DJH/123123/123/76dtHg7yYQ+LHws0xBUmqUrM5bdW"
                },
                "s3":{
                    "s3SchemaVersion":"1.0",
                    "configurationId":"677496ca-4ead-123-123-123",
                    "bucket":{
                    "name":"my-bucket-name",
                    "ownerIdentity":{
                        "principalId":"A3123123AR5"
                    },
                    "arn":"arn:aws:s3:::my-bucket-name"
                    },
                    "object":{
                    "key":file_name,
                    "size":24,
                    "eTag":"06a83081d2bb215",
                    "sequencer":"0060CCC3C"
                    }
                }
            }
        ]
    }