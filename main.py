from typing import Optional
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse # json 형식으로 데이터 전달
from typing import Union
from fastapi.responses import FileResponse
# html파일같은거 전송해주고 싶을때 요거 improt 해야함.

from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
from torchvision import transforms
from ultralytics import YOLO
from pydantic import BaseModel

# 나중에 요기위에다 DB접속해 주세요~~ 코드 넣어라.

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# "/" 로 접속했을시
@app.get('/')
def home() :
    return "JINI HI!"



############### 모델 코드 테스트

# 그래서 clas 생성해줌.
class SelectModel(BaseModel):
    # 데이터 타입 정의
    model : str


async def runYoloModel (file: UploadFile = File(...)):
     try:
        # YOLO 모델 로드
        model = YOLO(r'.\best.pt')
        model.predict(r'.\images\E3S690_20221011_02830841_M_Bullet_005-008_Cable_575-063_2.png', device='0',save=True,conf=0.5)  # 실시간분석에서 날아온 이미지가 여기 들어가야한다.
        image_bytes = await file.read()
       # outputs = get_prediction(image_bytes)
        # return JSONResponse(content={"predictions": outputs})
        return "test"
     except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    

@app.post("/receive_model")
async def predict(Model : SelectModel = Depends()):
    print(Model.model)
    runYoloModel()


#  실시간분석에서 날아온 이미지분석
@app.get("/analyze")
async def imgAnalyze() :
    # print(img)
    try:
        # YOLO 모델 로드
        model = YOLO(r'.\best.pt')
        model.predict('./images/E3S690_20221011_02830841_M_Bullet_005-008_Cable_575-063_2.png', device='0',save=True,conf=0.5)  # 실시간분석에서 날아온 이미지가 여기 들어가야한다.
        # image_bytes = await file.read()
        # outputs = get_prediction(image_bytes)
        # return JSONResponse(content={"predictions": outputs})
        return "test"
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




# "/index" 로 접속했을시 html파일 전송함.
@app.get('/index')
def index() :
    return FileResponse("index.html")


# "/data" 로 접속했을시
@app.get("/data")
def data () :
    return {"hello": 12345}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
# 웹 브라우저로 http://127.0.0.1:8000/items/5?q=test에 접속해봅시다!
# {item_id: 5, q: "test"}로 출력. 


from pydantic import BaseModel
# 서버로 데이터 받을려면 model이 필요하다. 위코드 improt 해와야함.

db = []
posts = {
    1: {"title": "첫 번째 제목", "content": "첫번째 글입니다.", "published": True, "rating": 5},
    2: {"title": "두 번째 제목", "content": "두번째 글입니다.", "published": True, "rating": 4}
}

# 블로그 포스트 모델
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# 그래서 clas 생성해줌.
class PostModel(BaseModel):
    # 데이터 타입 정의
    name : str
    content : str
    phone: str


# 서버로 데이터 받을려면 model이 필요하다.
# /send로  (name : str  content : str  phone: int) 요 데이터들을 보낼수 있음.
@app.post("/send/new")
def testSend(data : PostModel) : 
   # print(data)  # 보낸데이터 data에 담김. 
  #  return '전송완료'
    return data


# 전체 목록 보여줌.
@app.get("/posts")
def get_all_posts():
    return list(posts.values())


@app.get("/posts/{post_id}")
def get_post(post_id : int):
    if post_id not in posts:
        # raise는 예외를 발생시키는데 사용되는 키워드이다.
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[post_id]


# 새로운글 생성
@app.post("/posts/new")
def create_post(post: Post):
    print(post)
    post_id = len(posts)+1
    posts[post_id] = post.dict() # 딕셔너리로 바까서 추가해준다.
    return {"post_id": post_id, **post.dict()}  # ** 는 JS의 전개 연산자와 같은기능 같다.


# 글수정
@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post: Post):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts[post_id] = updated_post.dict()
    return {"post_id": post_id, **updated_post.dict()}



# db에서 데이터 꺼내오고 싶을때
@app.get('/getdb')
async def home() :
    # 참고로 async / await 키워드로 비동기 처리기능 사용.
   # await ~~~~
    # 이안에서 db에서 데이터 꺼내주세요~~ 등 db입출력 코드 작성.
    return "JINI HI!"



# 그래서 clas 생성해줌.
class SendToFastApiDto(BaseModel):
    # 데이터 타입 정의
    nickname : str
    fileId : str


# Spring 과 FastAPI 통신 테스트
# !! 주의 경로는 위에 Spring에서 적은 경로와 같아야함 !!
@app.post('/receive_string')
async def receive_string(requestDto: SendToFastApiDto) :
    print(requestDto)
    
    #Spring으로부터 JSON 객체를 전달받음
    dto_json = requestDto
	
   	#Spring에서 받은 데이터를 출력해서 확인
   # print(dto_json)
    
    #Spring으로 response 전달
    return "jini"



@app.post('/receive_string')
async def receive_string(requestDto: SendToFastApiDto) :
    print(requestDto)
    
    #Spring으로부터 JSON 객체를 전달받음
    dto_json = requestDto
	
   	#Spring에서 받은 데이터를 출력해서 확인
   # print(dto_json)
    
    #Spring으로 response 전달
    return "jini"


@app.post('/gospring')
async def gospring(requestDto: SendToFastApiDto) :
    print(requestDto)
    
    #Spring으로부터 JSON 객체를 전달받음
    dto_json = requestDto
	
   	#Spring에서 받은 데이터를 출력해서 확인
   # print(dto_json)
    
    #Spring으로 response 전달
    return "test ok"


# 서버 시작 명령
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


