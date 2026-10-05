from gradio_client import Client

print("Connecting to FLUX Space...")

client = Client("black-forest-labs/FLUX.1-dev")

print("Connected!")

result = client.predict(
    prompt="A cinematic movie pre-release event, dramatic red carpet, glowing spotlights, elegant cinema atmosphere, premium film premiere stage, realistic photography, rich depth, professional event poster artwork",
    seed=42,
    randomize_seed=True,
    width=768,
    height=1024,
    guidance_scale=3.5,
    num_inference_steps=20,
    api_name="/infer"
)

print("Generation completed!")

print("RESULT TYPE:")
print(type(result))

print("\nRESULT:")
print(result)