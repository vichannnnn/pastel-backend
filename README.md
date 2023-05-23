This backend service is dependent on the pastel-mix service from Hugging Face.
Assuming that NVIDIA Docker is set-up in your environment:

```bash
docker run -d --name pastel-mix --network internal-network -p 5000:5000 --gpus=all --restart=always r8.im/elct9620/pastel-mix@sha256:ba8b1f407cd6418fa589ca73e5c623c081600ecff19f7fc3249fa536d762bb29
```

You will need to run the commands above before starting this service.
