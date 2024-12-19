# globant-challenge

# AWS Management Scripts with Boto3

This repository contains Python scripts that utilize **Boto3** to interact with AWS services. Each script follows **PEP8 standards**, includes unit tests, and provides a short description and usage information. These scripts demonstrate general knowledge of Python, AWS, and Boto3.

---

## **Contents**

The project is divided into the following modules:

| Name           | Source            | Description                                                                                      |
|----------------|-------------------|--------------------------------------------------------------------------------------------------|
| **[s3](#s3)**  | `./s3/app`        | Checks if S3 buckets have public access. Removes public access if found.                        |
| **[rds](#rds)**| `./rds/app`       | Checks if RDS instances have public access. Removes public access if found.                     |
| **[ec2](#ec2)**| `./ec2/app`       | Checks if EC2 instances have the SSM policy assigned. Removes the policy from affected instances. |
| **[get-url](#get-url)** | `./get-url` | Contains utility scripts for URL-related tasks.                                                  |

---

## **Modules**

### **S3 Module**
- **Source**: `./s3/app`
- **Description**: 
  - This script lists all S3 buckets, checks their public access settings, and removes public access if it is enabled.
- **Usage**:
  ```bash
  python app/s3_block_public_access.py
