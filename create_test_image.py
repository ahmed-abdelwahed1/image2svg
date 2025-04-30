from PIL import Image

# Create a simple 100x50 red rectangle PNG image
img = Image.new('RGB', (100, 50), color = 'red')
img.save('/home/ubuntu/test_input.png')

print("Test image /home/ubuntu/test_input.png created.")

