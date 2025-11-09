# Jeffrey Code Portfolio

## PDF Analysis DevOps Project

This project processes PDF documents to extract and analyze keyword frequencies, storing results in a PostgreSQL database.

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python setup.py
   ```

2. **Start services with Docker:**
   ```bash
   docker-compose up -d
   ```

3. **Add PDF files to the `data/` directory**

4. **Run the processing pipeline:**
   ```bash
   python app/process_pdfs.py
   ```

### Project Structure

- `app/process_pdfs.py` - Main processing script
- `data/` - Directory for PDF files
- `scripts/init.sql` - Database schema
- `docker-compose.yml` - Container orchestration
- `.env` - Environment configuration
