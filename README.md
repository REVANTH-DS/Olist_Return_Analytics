# 🛒 E-Commerce Product Return Rate & Refund Leakage Analytics

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Data Analytics, Applied Statistics, and Machine Learning pipeline designed to quantify financial loss from product returns, evaluate logistics fulfillment bottlenecks, and segment customer return behaviors using the public **Olist Brazilian E-Commerce Dataset** (113,314 transactional records).

---

## 📱 Interactive Dashboard Showcase

The decision-support web portal built with **Streamlit** and **Plotly** provides real-time financial tracking and operational insights.

### 1. Executive Summary & Cluster Breakdown
![Dashboard Overview](assets/dashboard_overview.png)

### 2. Logistics Root-Cause & Payment Method Analysis
![Logistics Analysis](assets/logistics_analysis.png)

---

## 📌 Executive Summary & Key Results

Standard e-commerce metrics focus heavily on sales volume and binary customer churn—frequently missing the **silent profit killer: unrecovered return freight loss and refund leakage**. This project addresses that gap by engineering a proxy for hidden returns, running statistical hypothesis tests on logistics friction, and building an interactive executive decision-support portal.

### 📊 Core Project Metrics
* **Total Financial Leakage Identified:** **\$3,495,983.90** (Total value lost to cancellations and severe product defect returns)
* **Overall Return Proxy Rate:** **12.69%** across 113,314 processed transactions
* **Unrecoverable Freight Loss:** **\$304,983.12** in sunk shipping expenses
* **Statistical Significance:** Chi-Square ($\chi^2$) Test of Independence yielded $\chi^2 = 11,471.29$ ($p < 0.001$), mathematically confirming that delivery delays directly drive return rates.

---

## 🏗 System Architecture & Workflow

The architecture follows a decoupled, modular design separating raw ingestion, feature engineering, statistical modeling, machine learning clustering, and visualization.
