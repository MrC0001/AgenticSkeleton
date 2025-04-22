#!/bin/bash

# Set colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  Prompt Enhancement API Demonstration     ${NC}"
echo -e "${BLUE}============================================${NC}"

# Function to make a request and format the response
make_request() {
    local user_id="$1"
    local prompt="$2"
    local description="$3"

    echo -e "\n${YELLOW}>> $description (User: $user_id)${NC}"
    echo -e "${CYAN}Prompt:${NC} $prompt"

    # Escape the prompt for JSON
    json_payload=$(printf '{"user_id": "%s", "prompt": "%s"}' "$user_id" "$(echo "$prompt" | sed 's/"/\\"/g')")

    # Make the request and format the output
    curl -s -X POST http://localhost:8000/enhance_prompt \
      -H "Content-Type: application/json" \
      -d "$json_payload" | python3 -c "
import sys, json, textwrap

try:
    data = json.load(sys.stdin)
    if 'enhanced_response' in data:
        print('\\n${GREEN}Enhanced Response:${NC}')
        # Use textwrap for better readability of potentially long responses
        wrapped_response = textwrap.fill(data['enhanced_response'], width=100, initial_indent='  ', subsequent_indent='  ')
        print(wrapped_response)
    elif 'error' in data:
        print(f'\\n${YELLOW}Error:${NC} {data.get('error')}')
        print(f'  ${GRAY}{data.get('message')}${NC}')
    else:
        print('\\n${YELLOW}Unexpected Response Format:${NC}')
        print(data)
except json.JSONDecodeError:
    print('\\n${YELLOW}Error:${NC} Received non-JSON response from server.')
except Exception as e:
    print(f'\\n${YELLOW}Error processing response:${NC} {e}')
"

    echo -e "\n${BLUE}--------------------------------------------${NC}"
}

# --- Example Calls ---

# Example 1: Beginner user asking about mortgages
make_request "user002" "Tell me about mortgages for first-time buyers." "Beginner User - Mortgage Query"

# Example 2: Intermediate user asking about career growth
make_request "user001" "How can I use the internal mobility program to find a new role in data science?" "Intermediate User - Career Growth"

# Example 3: Expert user asking about SMB services
make_request "user005" "Provide a strategic overview of our SMB loan products compared to market trends." "Expert User - SMB Strategy"

# Example 4: Ambassador trainee asking about promotion
make_request "user004" "What are the key talking points for the new digital banking platform I should use with colleagues?" "Ambassador Trainee - Promotion"

# Example 5: Unknown user (defaults to Beginner)
make_request "user999" "What is brand advocacy?" "Unknown User - Basic Query"

# Example 6: Request likely to trigger multiple RAG entries
make_request "user001" "Explain the FlexiHome mortgage and how it relates to the digital platform." "Intermediate - Multi-Topic Query"

echo -e "\n${BLUE}============================================${NC}"
echo -e "${CYAN}Demonstration complete! The examples above showcase the${NC}"
echo -e "${CYAN}prompt enhancement capabilities, including skill-based${NC}"
echo -e "${CYAN}adjustments and RAG context/extras (using mock data).${NC}"
echo -e "${BLUE}============================================${NC}"