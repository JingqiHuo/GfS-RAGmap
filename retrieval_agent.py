from sentence_transformers import SentenceTransformer
import faiss
import cx_Oracle
from secrets_retrieval import get_password
import torch
import os
import json

class database_query:
    _model = None
    _index = None
    _metadata = None
    _conn = None
    _cursor = None

    def __init__(self):
        
        self.init_resources()


    @classmethod
    def init_resources(cls):
        print("initializing model...")
        cls.INDEX_PATH = "/home/s2630332/gfs/gazetteer.index"
        cls.META_PATH = "/home/s2630332/gfs/gazetteer_metadata.json"

        # 1. load embedding model
        if cls._model is None:
            print("Loading embedding model...")
            cls.model = SentenceTransformer('all-MiniLM-L6-v2')  # output demension 384
            print("Device:", cls.model.device)  # check computing device type (cpu/gpu)
            print("CUDA available:", torch.cuda.is_available())
            print("GPU device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
            print('Successfullt loaded embedding model.')

        # 2. connect to oracle db
        if cls._conn is None or cls._cursor is None:
            print("Connecting to Oracle database...")
            cls.password = get_password('/home/s2630332/gfs/ApiKeys/database.txt')
            cls.conn = cx_Oracle.connect(user="s2630332", password=cls.password, dsn="geosgen")
            cls.cursor = cls.conn.cursor()
            print('Successfully connected to Oracle database.')
    
        # 3. read data from SQL tables
            cls.cursor.execute("SELECT SEQNO, NAME FROM ops$scotgaz.towns ORDER BY SEQNO ASC")
            cls.rows = cls.cursor.fetchall()
            print('Successfully get metadata from gazetteer.')
        
        if cls._index is None or cls._metadata is None:
        # 4. check/construct the metadata
            print("Constructing text embedding and metadata...")
            cls.text_embedding = []
            cls.metadata = []
            for seqno, name in cls.rows:
                cls.text_embedding.append(f"{name}")  # customize embedding contents
                cls.metadata.append({"SEQNO": seqno, "NAME": name})
            print('Successfully constructed text embedding and metadata')

        # 4.5 Try to load existing index and metadata
        cls.index = None
        cls.rebuild = False

        if os.path.exists(cls.INDEX_PATH) and os.path.exists(cls.META_PATH):
            print("Trying to load existing index and metadata")
            try:
                # Load Index
                cls.index = faiss.read_index(cls.INDEX_PATH)

                # Load metadata
                with open(cls.META_PATH, "r") as f:
                    cls.meta_loaded = json.load(f)

                # See if the number of entries matches
                if len(cls.meta_loaded) != len(cls.text_embedding):
                    print("Number of entries does not match, trying to rebuild index...")
                    cls.rebuild = True
                else:
                    cls.metadata = cls.meta_loaded
                    print("Embeddings index and metadata loaded successfully.")
            except Exception as e:
                print(f"Load failed: {e}")
                cls.rebuild = True
        else:
            print("Cannot find index and metadata files, ready to rebuild.")
            cls.rebuild =True
        # if there's no exisiting index/current index won't work 
        if cls.rebuild:
    # 5. generate embedding vectors
            print('Trying to rebuild embeddings.')
            cls.embeddings = cls.model.encode(
                cls.text_embedding,
                convert_to_numpy=True,
                batch_size=128,               # 32 / 64 / 128
                show_progress_bar=True       
            )

    # 6. construct FAISS index
            print('Trying to rebuild FAISS index.')
            cls.index = faiss.IndexFlatL2(cls.embeddings.shape[1])  # use L2 dist
            cls.index.add(cls.embeddings)

    # 7. save the index file and metadata（for loading directly）
            print("Saving index and metadata")
            faiss.write_index(cls.index, "gazetteer.index")
            with open("gazetteer_metadata.json", "w") as f:
                json.dump(cls.metadata, f)
        

    def rag_workflow(self,query):
        print("RAG starts.")
        #print(f"The user is asking {self.query}")
        self.query = query
        query_embedding = self.model.encode([self.query], convert_to_numpy=True)

        top_k=1
        

# D=distance(the smaller, the more similar)
# I=index(referring to the vectors in .index file)
        D, I = self.index.search(query_embedding, top_k)
        result = []
        for idx in I[0]:
            result = self.metadata[idx]
            print(f"SEQNO:{result['SEQNO']},NAME:{result['NAME']}")
            self.cursor.execute(f"SELECT INTRODUCTION FROM ops$scotgaz.towns WHERE SEQNO = {result['SEQNO']}")
            intro = self.cursor.fetchall()[0]
            self.cursor.execute(f"SELECT CONV_LAT, CONV_LONG FROM ops$scotgaz.towns WHERE SEQNO = {result['SEQNO']}")
            coord = self.cursor.fetchall()[0]
            text = f"{coord} {intro}"
            geo_info = f"{result['NAME']}:{coord}"
        # 8. clean up resources
        print("Retrieval ends")
        #self.cursor.close()
        #self.conn.close()
        return text, geo_info


# next steps:
# 1) think about how to recognize entity's type (towns/geofeatures)
# 2) think about how to deal with multiple results/single result