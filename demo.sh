#!/bin/bash

# Set colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}    AgenticSkeleton API Demonstration      ${NC}"
echo -e "${BLUE}============================================${NC}"

# Function to make a request and format the response
make_request() {
    local request="$1"
    local description="$2"
    
    echo -e "\n${YELLOW}>> $description${NC}"
    echo -e "${CYAN}Request:${NC} $request"
    
    # Make the request and format the output
    curl -s -X POST http://localhost:8000/run-agent \
      -H "Content-Type: application/json" \
      -d "{\"request\": \"$request\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)

# Print plan
print('\\n${GREEN}Plan:${NC}')
for i, task in enumerate(data['plan']):
    print(f'  ${YELLOW}{i+1}.${NC} {task}')

# Print results
print('\\n${GREEN}Results:${NC}')
for i, result in enumerate(data['results']):
    print(f'  ${YELLOW}Task {i+1}:${NC} {result[\"subtask\"]}')
    if 'result' in result:
        preview = result['result'][:150] + '...' if len(result['result']) > 150 else result['result']
        print(f'    ${GRAY}{preview}${NC}')
"
    
    echo -e "\n${BLUE}--------------------------------------------${NC}"
}

# Run all the examples in sequence
make_request "Design a machine learning system for predictive maintenance in manufacturing" "AI/ML Domain Example"
make_request "Develop a telehealth monitoring system for remote patient care" "Healthcare Tech Domain Example"
make_request "Write a blog post about the impact of AI on job markets" "Writing Task Example"
make_request "Analyze recent trends in cryptocurrency markets" "Data Analysis Example"
make_request "Develop a REST API for an e-commerce platform" "Development Task Example"

echo -e "\n${BLUE}============================================${NC}"
echo -e "${CYAN}Demonstration complete! The examples above showcase the${NC}"
echo -e "${CYAN}mock response generation capabilities of AgenticSkeleton.${NC}"
echo -e "${BLUE}============================================${NC}"