from bs4 import BeautifulSoup
import sys

file_path = r'C:\Users\정현\.gemini\antigravity-ide\brain\258eb7f2-1436-40ba-8f31-94ed56fa9f38\.system_generated\steps\18\content.md'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    # Naver blogs usually store main text in se-main-container or postViewArea
    main_container = soup.find('div', class_='se-main-container')
    if not main_container:
        main_container = soup.find('div', id='postViewArea')
        
    if main_container:
        text = main_container.get_text(separator='\n', strip=True)
        print("--- CONTENT FOUND ---")
        print(text)
    else:
        print("--- NO MAIN CONTAINER FOUND, FULL TEXT ---")
        # Just print everything
        text = soup.get_text(separator='\n', strip=True)
        print(text)
except Exception as e:
    print(f"Error: {e}")
