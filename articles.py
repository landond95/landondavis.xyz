import os
import shutil
from bs4 import BeautifulSoup

# Define directories and file paths
queue_dir = "/var/www/landondavis/queue"
articles_dir = "/var/www/landondavis/articles"
articles_html = "/var/www/landondavis/articles.html"

def get_h2_from_html(file_path):
    """Extract the text of the first <h2> tag from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            h2 = soup.find('h2')
            return h2.text.strip() if h2 else "Untitled"
    except Exception as e:
        print(f"Error reading <h2> from {file_path}: {e}")
        return "Untitled"

def update_articles_html(filename, h2_text):
    """Add a new <h3> link to articles.html at the top of the <body>, ensuring each <h3> is on its own line."""
    try:
        # Read the existing articles.html
        with open(articles_html, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Create new <h3> link
        new_h3 = soup.new_tag('h3')
        new_link = soup.new_tag('a', href=f'./articles/{filename}')
        new_link.string = h2_text
        new_h3.append(new_link)

        # Find the body and insert the new <h3> after the <h1>
        body = soup.body
        if body:
            h1 = body.find('h1')
            if h1:
                h1.insert_after(new_h3)
            else:
                body.insert(0, new_h3)

        # Write the updated HTML with proper formatting
        with open(articles_html, 'w', encoding='utf-8') as f:
            # Use prettify() to format HTML, then clean up to ensure <h3> tags are on separate lines
            formatted_html = soup.prettify()
            # Split and rejoin lines to ensure each <h3> is isolated
            lines = formatted_html.splitlines()
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.rstrip())
                # Add a blank line after each </h3> to ensure separation
                if line.strip().endswith('</h3>'):
                    cleaned_lines.append('')
            f.write('\n'.join(cleaned_lines))
        print(f"Added <h3> link for {filename} with text '{h2_text}' to {articles_html}")

    except Exception as e:
        print(f"Error updating {articles_html}: {e}")

def process_queue():
    """Check queue directory, move files to articles, and update articles.html."""
    try:
        # Ensure directories exist
        if not os.path.exists(queue_dir):
            print(f"Queue directory {queue_dir} does not exist.")
            return
        if not os.path.exists(articles_dir):
            os.makedirs(articles_dir)
            print(f"Created articles directory {articles_dir}")

        # Get list of files in queue
        queue_files = [f for f in os.listdir(queue_dir) if os.path.isfile(os.path.join(queue_dir, f))]

        if not queue_files:
            print(f"No files found in {queue_dir}")
            return

        # Process each file
        for filename in queue_files:
            queue_path = os.path.join(queue_dir, filename)
            articles_path = os.path.join(articles_dir, filename)

            # Get <h2> text from the file
            h2_text = get_h2_from_html(queue_path)

            # Move file to articles directory
            shutil.move(queue_path, articles_path)
            print(f"Moved {filename} to {articles_dir}")

            # Update articles.html with new <h3> link
            update_articles_html(filename, h2_text)

    except Exception as e:
        print(f"Error processing queue: {e}")

if __name__ == "__main__":
    process_queue()