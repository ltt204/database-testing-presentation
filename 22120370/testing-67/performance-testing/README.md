# OrangeHRM Performance Testing Suite

This directory contains JMeter performance test scripts for testing the OrangeHRM Timesheet workflow.

## Directory Structure

```
performance-testing/
├── jmeter-scripts/          # JMeter test plan files (.jmx)
│   ├── leave_application_load.jmx
│   ├── leave_application_stress.jmx
│   └── leave_application_spike.jmx
├── test-data/               # Test data files
│   ├── users.csv           # User credentials (gitignored)
│   └── README.md           # Instructions for creating CSV
└── results/                 # Test execution results (generated)
```

## Prerequisites

### 1. Install Apache JMeter

**Download JMeter:**

```bash
# Visit https://jmeter.apache.org/download_jmeter.cgi
# Or use wget:
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
sudo mv apache-jmeter-5.6.3 /opt/jmeter
```

**Add to PATH (optional):**

```bash
echo 'export PATH=$PATH:/opt/jmeter/bin' >> ~/.bashrc
source ~/.bashrc
```

**Verify installation:**

```bash
jmeter --version
```

### 2. Install JMeter Plugins (Required for Stress & Spike Tests)

The Stress and Spike tests use custom thread groups from JMeter Plugins Manager:

- **Stepping Thread Group** (for Stress Test)
- **Ultimate Thread Group** (for Spike Test)

**Install using Plugins Manager:**

1. Download [Plugins Manager JAR](https://jmeter-plugins.org/get/)
2. Place it in `/opt/jmeter/lib/ext/`
3. Restart JMeter
4. Go to Options → Plugins Manager → Available Plugins
5. Install "Custom Thread Groups"

**Alternative - Download plugins directly:**

```bash
cd /opt/jmeter/lib/ext/
wget https://jmeter-plugins.org/files/packages/jpgc-casutg-2.10.zip
unzip jpgc-casutg-2.10.zip
```

### 3. Prepare Test Data

Create `test-data/users.csv` with the following content:

```csv
username,password
admin,admin123
```

### 4. Ensure OrangeHRM is Running

```bash
# Check Docker containers
docker ps | grep orangehrm

# If not running, start them:
cd /home/ltt204/study/database-testing-presentation
docker-compose up -d

# Verify OrangeHRM is accessible
curl -I http://localhost:8080
```

---

## Running Performance Tests

### Option 1: GUI Mode (Recommended for Debugging)

**Load Test:**

```bash
cd final-project/ltt204/performance-testing/jmeter-scripts
jmeter -t leave_application_load.jmx
```

**Stress Test:**

```bash
jmeter -t leave_application_stress.jmx
```

**Spike Test:**

```bash
jmeter -t leave_application_spike.jmx
```

**In GUI Mode:**

1. Click the green "Start" button (▶)
2. Monitor real-time results in listeners (Summary Report, View Results Tree, Response Time Graph)
3. After completion, review results and take screenshots

### Option 2: Command-Line Mode (Recommended for Production)

Running tests in non-GUI mode provides better performance and generates HTML reports.

**Load Test:**

```bash
cd final-project/ltt204/performance-testing/jmeter-scripts
jmeter -n -t leave_application_load.jmx \
       -l ../results/load_test_results.jtl \
       -e -o ../results/load_test_dashboard
```

**Stress Test:**

```bash
jmeter -n -t leave_application_stress.jmx \
       -l ../results/stress_test_results.jtl \
       -e -o ../results/stress_test_dashboard
```

**Spike Test:**

```bash
jmeter -n -t leave_application_spike.jmx \
       -l ../results/spike_test_results.jtl \
       -e -o ../results/spike_test_dashboard
```

**View Results:**

```bash
# Open HTML dashboard in browser
xdg-open ../results/load_test_dashboard/index.html   # Load Test
xdg-open ../results/stress_test_dashboard/index.html  # Stress Test
xdg-open ../results/spike_test_dashboard/index.html   # Spike Test
```

---

## Test Scenarios Explained

### 1. Load Test (`leave_application_load.jmx`)

**Purpose:** Simulate normal expected traffic to validate system performance under typical load.

**Configuration:**

- **Users:** 50 concurrent users
- **Ramp-up:** 60 seconds (users gradually added)
- **Loops:** 2 iterations per user
- **Duration:** ~3-4 minutes

**Test Workflow:**

1. Get Login Page (GET /auth/login)
2. Submit Login (POST /auth/validate)
3. Navigate to Timesheet (GET /time/viewEmployeeTimesheet)
4. View My Timesheet (GET /time/viewMyTimesheet)

**Success Criteria:**

- Average response time < 2000ms
- Error rate < 1%
- All assertions pass

### 2. Stress Test (`leave_application_stress.jmx`)

**Purpose:** Find the breaking point by gradually increasing load beyond normal capacity.

**Configuration:**

- **Initial Users:** 10
- **Max Users:** 200
- **Step Increment:** Add 10 users every 30 seconds
- **Duration:** ~10 minutes

**What to observe:**

- At what point does response time degrade significantly?
- When do errors start occurring?
- System resource usage (CPU, memory, database connections)

**Expected Breaking Point:** 80-150 concurrent users (based on Docker resource limits)

### 3. Spike Test (`leave_application_spike.jmx`)

**Purpose:** Test system behavior during sudden traffic burst (e.g., start of workday).

**Configuration:**

- **Spike:** 0 → 100 users in 2 seconds
- **Hold:** 10 seconds at peak load
- **Ramp-down:** 2 seconds back to 0

**What to observe:**

- Does the system gracefully handle the spike?
- Are there connection errors or timeouts?
- How quickly does the system recover?

---

## Performance Thresholds

| Metric                      | Expected     | Acceptable    | Poor         |
| --------------------------- | ------------ | ------------- | ------------ |
| **Average Response Time**   | < 1000ms     | 1000-2000ms   | > 2000ms     |
| **90th Percentile**         | < 1500ms     | 1500-3000ms   | > 3000ms     |
| **Error Rate**              | 0%           | < 1%          | > 1%         |
| **Throughput**              | > 20 req/sec | 10-20 req/sec | < 10 req/sec |
| **Concurrent Users (Load)** | 50 users     | 30-50 users   | < 30 users   |
| **Breaking Point (Stress)** | > 100 users  | 80-100 users  | < 80 users   |

---

## Taking Screenshots for Report

When running in GUI mode, capture screenshots of:

1. **Summary Report** - Shows overall statistics (samples, average, min, max, error %)
2. **View Results Tree** - Shows detailed request/response for debugging
3. **Response Time Graph** - Visual representation of response times

**Screenshot Tips:**

- Run tests in GUI mode first to familiarize yourself
- Maximize the listener panels for clear screenshots
- Capture after test completion for final results
- Use command-line mode for actual performance data

---

## Troubleshooting

### Issue: "Cannot find users.csv"

**Solution:** Create the CSV file in `test-data/` directory with proper format.

### Issue: Connection refused

**Solution:** Verify OrangeHRM Docker container is running:

```bash
docker ps | grep orangehrm
curl http://localhost:8080
```

### Issue: Stepping/Ultimate Thread Group not found

**Solution:** Install JMeter Plugins as described in Prerequisites section.

### Issue: Out of memory errors

**Solution:** Increase JMeter heap size:

```bash
export JVM_ARGS="-Xms512m -Xmx2048m"
jmeter -n -t leave_application_load.jmx ...
```

### Issue: High error rate during tests

**Solution:**

- Reduce number of threads
- Increase ramp-up time
- Check OrangeHRM logs: `docker logs orangehrm_app`
- Verify database connection limits

---

## Data Backup (Important!)

Before running stress tests, back up your database:

```bash
# Create backup directory
mkdir -p backup

# Backup database volume
docker run --rm \
  -v database-testing-presentation_db_data:/data \
  -v $(pwd)/backup:/backup \
  ubuntu tar czf /backup/db_backup_$(date +%Y%m%d_%H%M%S).tar.gz /data

# Verify backup
ls -lh backup/
```

**Restore if needed:**

```bash
docker run --rm \
  -v database-testing-presentation_db_data:/data \
  -v $(pwd)/backup:/backup \
  ubuntu tar xzf /backup/db_backup_YYYYMMDD_HHMMSS.tar.gz -C /
```

---

## Next Steps

After running all tests:

1. Collect screenshots from all 3 report viewers for each test type
2. Analyze results and compare against thresholds
3. Document findings in `Performance_testing_report.pdf`
4. Include:
   - System specifications
   - Test methodology
   - Expected vs Actual results
   - Screenshots and graphs
   - Step-by-step instructions (this README)

---

**Author:** LTT204  
**Date:** 2026-01-09  
**OrangeHRM Version:** 5.8
