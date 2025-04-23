#!/bin/bash

# Set colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Default host and port
HOST=${API_HOST:-"localhost"}
PORT=${API_PORT:-"8000"}
BASE_URL="http://${HOST}:${PORT}"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Prompt Enhancement API Demonstration     ${NC}"
echo -e "${BLUE}  Targeting: ${BASE_URL}                 ${NC}"
echo -e "${BLUE}============================================${NC}"

# --- Health Check ---
echo -e "\n${YELLOW}>> Checking API Health...${NC}"
health_status=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health")
if [ "$health_status" -eq 200 ]; then
    echo -e "${GREEN}API is healthy! Status: $health_status${NC}"
    curl -s "${BASE_URL}/health" | python3 -m json.tool # Pretty print JSON response
else
    echo -e "${YELLOW}Error:${NC} API health check failed! Status: $health_status"
    echo -e "${GRAY}Is the server running at ${BASE_URL}?${NC}"
    exit 1
fi
echo -e "\n${BLUE}--------------------------------------------${NC}"


# Function to make a request and format the response
# Arguments:
# $1: Description of the request
# $2: User ID string
# $3: User prompt string
make_request() {
    local description="$1"
    local user_id="$2"
    local user_prompt="$3"

    # Add a more prominent separator
    echo -e "\n${YELLOW}#############################################${NC}"
    echo -e "${YELLOW}>> $description (User: ${CYAN}$user_id${YELLOW})${NC}"
    echo -e "${YELLOW}#############################################${NC}"
    echo -e "${CYAN}Original Prompt:${NC} $user_prompt"

    # Escaping quotes within the prompt for JSON safety
    escaped_prompt=$(echo "$user_prompt" | sed 's/"/\\"/g')
    json_payload=$(printf '{"user_id": "%s", "prompt": "%s"}' "$user_id" "$escaped_prompt")

    echo -e "${GRAY}Sending Payload:${NC} $json_payload"

    # Make the request and format the output using Python
    curl -s -X POST "${BASE_URL}/enhance_prompt" \
      -H "Content-Type: application/json" \
      -d "$json_payload" | python3 -c "
import sys, json, textwrap, re

# Define colors here to avoid backslash issues in f-strings
GREEN = '\\033[0;32m'
YELLOW = '\\033[1;33m'
GRAY = '\\033[0;90m'
CYAN = '\\033[0;36m'
BLUE = '\\033[0;34m' # Added Blue
BOLD = '\\033[1m'
NC = '\\033[0m' # No Color

def print_section(title, content, color=GRAY, indent='  '):
    print(f'{indent}{BOLD}{color}--- {title} ---{NC}')
    # Indent content lines, handle lists within content gracefully
    lines = content.strip().split('\\n')
    for line in lines:
        # Basic check if line looks like a list item
        if line.strip().startswith(('-', '*')):
             print(f'{indent}  {color}{line.strip()}{NC}')
        else:
            wrapped_lines = textwrap.fill(line, width=95, initial_indent=f'{indent}  ', subsequent_indent=f'{indent}  ')
            print(f'{color}{wrapped_lines}{NC}')

try:
    data = json.load(sys.stdin)
    if 'enhanced_response' in data:
        print(f'\\n{BOLD}{GREEN}--- Enhanced Response ---{NC}')
        response_text = data['enhanced_response']

        # Split the response into sections based on '--- ... ---' headers
        sections = re.split(r'(\\n\\s*--- .+? ---\\s*\\n)', response_text, flags=re.IGNORECASE)

        # The first element might be empty or initial text before the first header
        current_content = sections[0].strip()
        if current_content:
             # Print any initial text (like the Mock Mode header)
             print(f'  {GRAY}{current_content}{NC}')


        # Process pairs of (header, content)
        for i in range(1, len(sections), 2):
            header_full = sections[i].strip()
            content = sections[i+1].strip()

            # Extract title from header like '--- Title ---'
            match = re.match(r'--- (.+?) ---', header_full)
            title = match.group(1) if match else 'Section'

            # Assign colors based on title keywords
            section_color = GRAY # Default
            if 'Prompt' in title: section_color = CYAN
            if 'Guidance' in title: section_color = YELLOW
            if 'Context' in title: section_color = BLUE
            if 'Restrictions' in title: section_color = YELLOW
            if 'Offers' in title: section_color = GREEN
            if 'Tips' in title: section_color = GREEN
            if 'Documents' in title: section_color = BLUE


            print_section(title, content, color=section_color)


        # Print the final closing line if it exists
        if '--- End Mock LLM Response ---' in response_text:
             print(f'  {GRAY}--- End Mock LLM Response ---{NC}')


        print(f'{BOLD}{GREEN}-------------------------{NC}') # Add footer

    elif 'error' in data: # Handle potential API error structure
        print('\\n' + YELLOW + 'API Error:' + NC + ' ' + str(data.get('error', 'N/A')))
        print('  ' + GRAY + str(data.get('message', 'N/A')) + NC)

    elif 'detail' in data: # Handle FastAPI validation error structure
        print('\\n' + YELLOW + 'Validation Error:' + NC)
        detail_str = json.dumps(data['detail'], indent=2)
        for line in detail_str.splitlines():
            print('  ' + GRAY + line + NC)

    else:
        print('\\n' + YELLOW + 'Unexpected Response Format:' + NC)
        print(json.dumps(data, indent=2))

except json.JSONDecodeError:
    print('\\n' + YELLOW + 'Error:' + NC + ' Received non-JSON response from server.')
except Exception as e:
    print('\\n' + YELLOW + 'Error processing response:' + NC + ' ' + repr(e))
"

    # Keep the original separator at the end of the function call section
    echo -e "\n${BLUE}--------------------------------------------${NC}"
}

# --- Example Calls ---

# Example 1: Simple request (using a known user ID)
make_request "Simple Query" \
             "user001" \
             "Tell me about Python decorators."

# Example 2: Beginner user asking about mortgages (using specific user ID)
make_request "Beginner User - Mortgage Query" \
             "user002" \
             "Tell me about mortgages for first-time buyers."

# Example 3: Intermediate user with preferences (using specific user ID)
make_request "Intermediate User - Career Growth" \
             "user001" \
             "How can I use the internal mobility program to find a new role in data science?"

# Example 4: Expert user with context (using specific user ID)
make_request "Expert User - SMB Strategy" \
             "user005" \
             "Provide a strategic overview of our SMB loan products compared to market trends."

# Example 5: Ambassador trainee (using specific user ID)
make_request "Ambassador Trainee - Promotion" \
             "user004" \
             "What are the key talking points for the new digital banking platform I should use with colleagues?"

# Example 6: Unknown user (defaults to Beginner)
make_request "Unknown User - Basic Query" \
             "user999" \
             "What is brand advocacy?"

# Example 7: Request likely to trigger multiple RAG entries
make_request "Intermediate - Multi-Topic Query" \
             "user001" \
             "Explain the FlexiHome mortgage and how it relates to the digital platform."

echo -e "\n${BLUE}============================================${NC}"
echo -e "${CYAN}Demonstration complete!${NC}"
echo -e "${BLUE}============================================${NC}"