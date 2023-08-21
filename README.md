1.Download Docker Desktop and run it

2.Open Terminal (Mac / Linux) or CMD (Windows)

3.Download / Git clone this repo in Terminal / CMD:
git clone https://github.com/polylam1994/LangChain_ChatPDF.git

4.Place your OpenAI key to 'YOUR-KRY' in LangChain_ChatPDF.py 
os.environ['OPENAI_API_KEY'] = 'YOUR-KEY'

5.Navigate to the cloned repository:
cd your-path/LangChain_ChatPDF

6.Build the Docker image:
docker build -t your_image_name .

7.Run the Docker container on port 5000 with the following command:
docker run -p 5000:5000 your_image_name
