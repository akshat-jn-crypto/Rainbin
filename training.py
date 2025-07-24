from ultralytics import YOLO


model = YOLO("yolov9c.pt")  
results = model.train(data="data.yaml", epochs=5)                   ## for CPU
# results = model.train(data="data.yaml", epochs=10, device="cuda")  ## for GPU
# results = model.train(data="data.yaml", epochs=10, device="mps")   ## for Apple Silicon 
model.export()
