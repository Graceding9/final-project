# Python Password Manager

A simple **local password manager** built with Python and Tkinter.  
It uses a **master password** to protect access and stores all account data in a local file encoded with **Base64**.

> ⚠️ **Security Warning**  
> Base64 is **not real encryption**. This project is for **learning/demo purposes only**.  
> Do **NOT** use it to store real, sensitive passwords in production environments.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Master Password](#master-password)
  - [Data Storage](#data-storage)
  - [Password Generation](#password-generation)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Run](#installation--run)
- [Usage Guide](#usage-guide)
  - [First Run: Set Master Password](#first-run-set-master-password)
  - [Login with Master Password](#login-with-master-password)
  - [Main Interface](#main-interface)
    - [Generate Password](#generate-password)
    - [Add / Update Entry](#add--update-entry)
    - [View All Passwords](#view-all-passwords)
    - [Search Website](#search-website)
    - [Delete Entry](#delete-entry)
- [Code Overview](#code-overview)
- [Limitations](#limitations)
- [Possible Improvements](#possible-improvements)
- [License](#license)

---

## Overview

This application is a **desktop GUI password manager** that allows you to:

- Protect access with a **master password**
- Store username/email and password for multiple websites
- Generate strong random passwords
- Search, view, and delete stored entries
- Persist data locally in an encoded file

The GUI is implemented using **Tkinter**, the standard GUI toolkit that ships with Python.

---

## Features

- 🔐 **Master Password Protection**
  - First launch: set a master password
  - Subsequent launches: login required with the correct master password

- 📝 **Add / Update Entries**
  - Each entry contains:
    - Website
    - Username / Email
    - Password (stored in encoded form)
  - If a website already exists, its entry is updated

- 🎲 **Password Generator**
  - Generates a random password containing:
    - Uppercase and lowercase letters
    - Digits
    - Symbols (punctuation)

- 🔍 **Search by Website**
  - Quickly search for a website
  - Display its username and **decoded** password in a popup window

- 📋 **View All Passwords**
  - View all stored entries
  - Displayed in a scrollable text window

- 🗑️ **Delete Entry**
  - Delete a specific website entry after user confirmation

- 💾 **Local Data Storage**
  - All entries are stored in a single file as JSON, encoded with Base64

---

## Tech Stack

- **Language:** Python 3
- **GUI Framework:** Tkinter
- **Data Format:** JSON (encoded as Base64 string)
- **Standard Libraries Used:**
  - `tkinter` (GUI)
  - `base64` (encoding/decoding)
  - `json` (data serialization)
  - `random`, `string` (password generation)
  - `os` (file existence checks)

---

## Project Structure

Assuming you save the provided code as `password_manager.py`:

```text
project_root/
├── password_manager.py      # Main application file
├── password_data.txt        # (Auto-created) Encoded password data
└── master_key.txt           # (Auto-created) Encoded master password
