# AWS S3 Block Public Access Script

This project contains a Python script that interacts with AWS to manage the Block Public Access settings of S3 buckets. The script lists S3 buckets, checks their public access settings, and disables public access if required. It also includes unit tests for core functions and a Docker setup for easy deployment.

---

## **Project Structure**

```plaintext
s3/
├── app/
│   ├── s3_block_public_access.py      # Main script to manage S3 public access
│   ├── test_s3_block_public_access.py # Unit tests for the script
├── Dockerfile                         # Docker configuration
├── requirements.txt                   # Python dependencies
