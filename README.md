# Simons Rock Course Scheduler Tool

## Setup and Usage

1. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Course Catalog**:  
   Run the following to create `courses.csv`:
   ```bash
   python course-puller.py
   ```
   To use a different catalog, update the `url` in `course-puller.py`.

3. **Run the Scheduler**:  
   Check for scheduling conflicts and AA requirements:
   ```bash
   python course-sched.py
   ```
   Follow prompts to enter CRNs or use a text file (e.g., `test.txt`):
   ```bash
   python course-sched.py < test.txt
   ```

## Files

- **`course-puller.py`**: Fetches and saves the course catalog as `courses.csv`.  
- **`course-shed.py`**: Checks scheduling conflicts and AA requirement completion.  
- **`test.txt`**: Example file for CRNs.

## Notes

- Ensure `courses.csv` exists before running `course-shed.py`.
- Update the `url` in `course-puller.py` to fetch a different course catalog.

## Acknowledgments
I used these playlist for reference with Pandas and Beautiful Soup 4 
1. [Beautiful Soup 4 Tutorial](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lSq2IDrA6vpZEV92AmQfJK) by Tech With Tim.  
2. [Pandas Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS) by Corey Schafer.
