import base64
from io import BytesIO
import json
import os
import random
from PIL import Image
from django.utils.safestring import mark_safe

class Utility:
    #TODO: try to migrate pulling the json objects in this file using cache.
    def __init__(self):
        self.topicVsQuestions = self.loadJsonData('./data/Topics.json')
        self.subjectVsQuestions = self.loadJsonData('./data/Subjects.json')
        self.Questions = self.loadJsonData('./data/Questions.json')
        print("loading data")
    def getQuestionDetails(self, qid):
        #print(self.Questions[qid])
        #pdfcontent=self.getQuestionPdf(qid)
        #self.Questions[qid]["QuestionPng"]=mark_safe(self.getdummyjpgimage()) #getQuestionPng(qid)
        qObject=[] #array that holds 5 images(base64 encoded) quesion, and 4 options.
        qObject.append(self.getQuestionPng(f'{1}._Question.png'))
        qObject.append(self.getQuestionPng(f'{1}.a.png'))
        qObject.append(self.getQuestionPng(f'{1}.b.png'))
        qObject.append(self.getQuestionPng(f'{1}.c.png'))
        qObject.append(self.getQuestionPng(f'{1}.d.png'))
        self.Questions[qid]["QuestionPng"]=qObject

        #TODO: Below will be ideally from response packet to be refactored.
        self.Questions[qid]["Choice"]="-1"
        self.Questions[qid]["duration"]="0"
        self.Questions[qid]["submitDuration"]="0"
        self.Questions[qid]["markedAsReview"]="0"
        return self.Questions[qid]

    def getQuestionPng(self,imageId):
        png_file_path = f"./data/Questions/{imageId}" 
        #print(png_file_path)
        if os.path.exists(png_file_path):
            with open(png_file_path, 'rb') as png_file:
                png_data = base64.b64encode(png_file.read()).decode('utf-8')
                #print(f"Image data: {png_data[:100]}...")
                return png_data

    def loadJsonData(self, filename):
        with open(filename) as f:
            return json.load(f)

    def createTest(self, subjects, topics, numQuestions):
        # Your logic to pull N number of questions equally distributed among the subjects and topics
        # Return the question IDs
        #ignore subjects for now in framing the questions.
        #print(subjects)
        #print(topics)
        #print(numQuestions)
        ret=[]#take anempty return array
        #for t in topics:
        #    print(t)
        #below is a base algorithm, and needs periodic improvizations
        #TODOs: check repetitions, equal distributions, eliminate solved questions etc.
        while len(ret)<numQuestions:
            randTopic=topics[random.randint(0,len(topics)-1)]
            #print(randTopic)
            nQsInTopic=len(self.topicVsQuestions[randTopic])-1
            qIdx=random.randint(0,nQsInTopic)
            randQId=self.topicVsQuestions[randTopic][qIdx]
            ret.append(randQId)
            pass
        #print(ret)
        #print(self.topicVsQuestions)
        return ret

    def Deprecatedgetdummyjpgimage(self):
        # Create a small JPEG image
        img = Image.new('RGB', (100, 100))
        img.putpixel((50, 50), (255, 0, 0))  # Draw a red pixel

        # Save the image to a bytes buffer
        buf = BytesIO()
        img.save(buf, format='JPEG')

        # Encode the image as Base64
        encoded_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        #encoded_img = "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"
        return encoded_img

    def DeprecatedgetQuestionPdf(self,question_id):
        #pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        #pdf_file_path = os.path.join(pdf_dir, f'{question_id}.pdf')
        pdf_file_path = f'./data/pdfs/1.pdf'

        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, 'rb') as pdf_file:
                return pdf_file.read()
        else:
            # Handle the case when the PDF file is not found
            return None
