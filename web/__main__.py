import uvicorn

if __name__ == "__main__":
    # nohup /opt/conda/envs/web/bin/python -u /opt/ml/web_final/web/__main__.py > /opt/ml/web_final.log &
    uvicorn.run("main:app", host="0.0.0.0", port=30001, reload=True)