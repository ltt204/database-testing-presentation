#!/bin/bash

# OrangeHRM Performance Test Runner
# Usage: ./run-tests.sh [load|stress|spike|all|download]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JMETER_SCRIPTS_DIR="$SCRIPT_DIR/jmeter-scripts"
RESULTS_DIR="$SCRIPT_DIR/results"

# JMeter local installation path
JMETER_VERSION="5.6.3"
JMETER_HOME="$SCRIPT_DIR/jmeter"
JMETER_BIN="$JMETER_HOME/bin/jmeter"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Download and install JMeter locally
download_jmeter() {
    echo -e "${BLUE}Downloading Apache JMeter ${JMETER_VERSION}...${NC}"

    local download_url="https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz"
    local archive="apache-jmeter-${JMETER_VERSION}.tgz"

    cd "$SCRIPT_DIR"

    # Download JMeter
    if command -v wget &> /dev/null; then
        wget -q --show-progress "$download_url" -O "$archive"
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar "$download_url" -o "$archive"
    else
        echo -e "${RED}Error: wget or curl is required to download JMeter${NC}"
        exit 1
    fi

    # Extract
    echo -e "${BLUE}Extracting JMeter...${NC}"
    tar -xzf "$archive"

    # Rename to simple folder name
    mv "apache-jmeter-${JMETER_VERSION}" jmeter

    # Clean up archive
    rm -f "$archive"

    echo -e "${GREEN}✓ JMeter ${JMETER_VERSION} installed to: $JMETER_HOME${NC}"
}

# Check if JMeter is available
check_jmeter() {
    if [[ -x "$JMETER_BIN" ]]; then
        echo -e "${GREEN}✓ JMeter found: $JMETER_HOME${NC}"
        return 0
    fi

    # Check if JMeter is in PATH as fallback
    if command -v jmeter &> /dev/null; then
        JMETER_BIN="jmeter"
        echo -e "${GREEN}✓ JMeter found in PATH${NC}"
        return 0
    fi

    echo -e "${RED}✗ JMeter not found${NC}"
    echo ""
    echo "JMeter is not installed. Run one of the following:"
    echo ""
    echo "  Option 1: Auto-download to local folder"
    echo "    ./run-tests.sh download"
    echo ""
    echo "  Option 2: Manual download"
    echo "    wget https://dlcdn.apache.org/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz"
    echo "    tar -xzf apache-jmeter-${JMETER_VERSION}.tgz"
    echo "    mv apache-jmeter-${JMETER_VERSION} jmeter"
    echo ""
    exit 1
}

# Check if OrangeHRM is running
check_orangehrm() {
    echo -n "Checking OrangeHRM availability... "
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 | grep -q "200\|302"; then
        echo -e "${GREEN}✓ OrangeHRM is running${NC}"
    else
        echo -e "${RED}✗ OrangeHRM is not accessible at http://localhost:8080${NC}"
        echo "Start it with: cd ../database-testing-presentation && docker-compose up -d"
        exit 1
    fi
}

# Create results directory
setup_results() {
    local test_type=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local result_dir="$RESULTS_DIR/${test_type}_${timestamp}"

    mkdir -p "$result_dir"
    echo "$result_dir"
}

# Run load test
run_load_test() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Running LOAD TEST (50 users, 60s ramp-up, 2 loops)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"

    local result_dir=$(setup_results "load")

    "$JMETER_BIN" -n -t "$JMETER_SCRIPTS_DIR/leave_application_load.jmx" \
           -l "$result_dir/results.jtl" \
           -e -o "$result_dir/dashboard" \
           -j "$result_dir/jmeter.log"

    echo -e "\n${GREEN}✓ Load test completed${NC}"
    echo -e "  Results: $result_dir/dashboard/index.html"
}

# Run stress test
run_stress_test() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Running STRESS TEST (200 users, 300s ramp-up)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"

    local result_dir=$(setup_results "stress")

    "$JMETER_BIN" -n -t "$JMETER_SCRIPTS_DIR/leave_application_stress.jmx" \
           -l "$result_dir/results.jtl" \
           -e -o "$result_dir/dashboard" \
           -j "$result_dir/jmeter.log"

    echo -e "\n${GREEN}✓ Stress test completed${NC}"
    echo -e "  Results: $result_dir/dashboard/index.html"
}

# Run spike test
run_spike_test() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Running SPIKE TEST (100 users, 2s ramp-up)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"

    local result_dir=$(setup_results "spike")

    "$JMETER_BIN" -n -t "$JMETER_SCRIPTS_DIR/leave_application_spike.jmx" \
           -l "$result_dir/results.jtl" \
           -e -o "$result_dir/dashboard" \
           -j "$result_dir/jmeter.log"

    echo -e "\n${GREEN}✓ Spike test completed${NC}"
    echo -e "  Results: $result_dir/dashboard/index.html"
}

# Run all tests
run_all_tests() {
    run_load_test
    run_stress_test
    run_spike_test

    echo -e "\n${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  All tests completed!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "\nResults saved to: $RESULTS_DIR"
}

# Show usage
show_usage() {
    echo "OrangeHRM Timesheet Performance Test Runner"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  download   Download and install JMeter locally"
    echo "  load       Run load test (50 concurrent users)"
    echo "  stress     Run stress test (up to 200 users)"
    echo "  spike      Run spike test (100 users in 2 seconds)"
    echo "  all        Run all tests sequentially"
    echo "  check      Check prerequisites only"
    echo ""
    echo "Examples:"
    echo "  $0 download      # Download JMeter first"
    echo "  $0 load          # Run only load test"
    echo "  $0 all           # Run all tests"
    echo "  $0 check         # Verify JMeter and OrangeHRM are ready"
}

# Main
main() {
    echo -e "${YELLOW}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     OrangeHRM Timesheet Performance Test Suite            ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    case "${1:-}" in
        download)
            download_jmeter
            ;;
        load)
            check_jmeter
            check_orangehrm
            run_load_test
            ;;
        stress)
            check_jmeter
            check_orangehrm
            run_stress_test
            ;;
        spike)
            check_jmeter
            check_orangehrm
            run_spike_test
            ;;
        all)
            check_jmeter
            check_orangehrm
            run_all_tests
            ;;
        check)
            check_jmeter
            check_orangehrm
            echo -e "\n${GREEN}All prerequisites met!${NC}"
            ;;
        *)
            show_usage
            exit 0
            ;;
    esac
}

main "$@"
