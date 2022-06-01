import uvicorn

if __name__ == "__main__":
    # nohup /opt/conda/envs/web/bin/python -u /opt/ml/recsys12/Backend/__main__.py > /opt/ml/web.log &
    uvicorn.run("main:app", host="0.0.0.0", port=30002, reload=True)