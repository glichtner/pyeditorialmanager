pyEditorialManager
==================

Python interface for the Aries Editorial Manager journal submission system at https://www.editorialmanager.com.

Currently supported:

- Main menu: Reading of number of submissions per category (e.g. "Submissions being processed")
- Pending submissions: Dates & status of pending submissions (e.g. "under review")
- Completed submissions: Dates & status of completed submissions (e.g. "accepted")

Not (yet) supported:

- Creation of new submissions
- Modification of existing submissions

Requirements
------------
- beautifulsoup
- pandas
- html5lib (because the responses of the editorialmanager are malformed HTML, the python html parser from beautifulsoup cannot be used)

Installation
------------
.. code-block:: python

    pip install editorialmanager

Usage
-----

.. code-block:: python

    from editorialmanager import Journal

    # instantiate the journal by using the abbreviation that is used by editorialmanager
    # For example: The journal "Critical Care" has the EditorialManager URL https://www.editorialmanager.com/cric/
    #   Therefore, the journal name to use here is "cric"
    cric = Journal('cric', username='my-username', password='my-password')

    # Get the overview of submissions per type/category from the main menu
    cric.overview()
    # Returns:
    '''
    |    | name                                      |   count | type            |
    |---:|:------------------------------------------|--------:|:----------------|
    |  0 | Submissions Sent Back to Author           |       0 | New Submissions |
    |  1 | Incomplete Submissions                    |       0 | New Submissions |
    |  2 | Submissions Waiting for Author's Approval |       0 | New Submissions |
    |  3 | Submissions Being Processed               |       1 | New Submissions |
    |  4 | Submissions Needing Revision              |       0 | Revisions       |
    |  5 | Revisions Sent Back to Author             |       0 | Revisions       |
    |  6 | Incomplete Submissions Being Revised      |       0 | Revisions       |
    |  7 | Revisions Waiting for Author's Approval   |       0 | Revisions       |
    |  8 | Revisions Being Processed                 |       0 | Revisions       |
    |  9 | Declined Revisions                        |       0 | Revisions       |
    | 10 | Submissions with a Decision               |       1 | Completed       |
    | 11 | Submissions with Production Completed     |       0 | Completed       |
    '''

    # Get information about currently pending submissions
    cric.pending_submissions()
    # Returns:
    '''
    |    | Manuscript Number   | Title              | Initial Date Submitted   | Status Date         | Current Status   |
    |---:|:--------------------|:-------------------|:-------------------------|:--------------------|:-----------------|
    |  0 | CRIC-x-xx-xxxx   x  | <Manuscript title> | 2020-12-02 00:00:00      | 2020-12-03 00:00:00 | Editor Invited   |
    '''

    # Get information about completed submissions
    cric.completed_submissions()
    # Returns:
    '''
    |    | Manuscript Number   | Title              | Initial Date Submitted   | Status Date         | Current Status        | Date Final Disposition Set   | Final Disposition   |
    |---:|:--------------------|:-------------------|:-------------------------|:--------------------|:----------------------|:-----------------------------|:--------------------|
    |  0 | CRIC-x-xx-xxxxx     | <Manuscript title> | 2016-07-03 00:00:00      | 2016-07-19 00:00:00 | Final Decision Reject | 2016-07-19 00:00:00          | Accept              |
    '''


Notes
-----
The actual displayed columns from pending and completed submissions are specified by each journal independently and
different columns maybe included or missing depending on the journal.

Author
------
Gregor Lichtner - `@glichtner <https://github.com/glichtner>`_
