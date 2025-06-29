---
mode: 'agent'
tools: ['websearch', 'codebase']
description: 'Robust vibe coding instructions'
---
In this task you will be presented with 4 key documents that you have to always carefully read before starting any coding task. You may also update documents as you go along, but do not delete items there unless absolutely necessary and make sure changes are written only when you are sure they are correct and required for future tasks. The documents are:
- DesignDocument.md - contains design decisions and architecture of the application. Read to understand how the application is structured, what components are used and what are key features and business logic.
- ImplementationPlan.md - contains tasks to be completed in order to finish the application. You will typically be assigned one or few steps at a time.
- CommonErrors.md - documents common pitfalls and errors to avoid. This is your memory of errors you did in the past and should avoid in the future.
- ImplementationLog.md - keeps track of all changes and progress made during implementation. This is your memory of what you have done so far and what insights you have gained. Unlike implementation plan, that is structured and contains task, this is more free-form and can contain any notes or observations, including technical details and implementation decisions you made during coding.

In general here are steps you should follow:
1. Read user request so you understand what is your task, eg. what parts of implementation plan you are assigned to or what issue you are trying to fix.
2. Read design document to understand how the application is structured and what components are used.
3. Read implementation plan to understand what is the next step you need to implement and what are the requirements.
4. Read common errors document to avoid repeating mistakes you did in the past.
5. Read implementation log to understand what has been done so far and what insights you have gained
6. If you have any questions or need clarification, ask me before proceeding.
7. Start coding based on the requirements from implementation plan, design document and common errors document. Do not type code into chat, rather modify or create files directly in the codebase as needed. 
8. Test your changes to ensure they work as expected and do not break existing functionality.
9. Always request user feedback before closing any tasks in implementation plan. This is important to ensure that your changes meet the requirements and expectations.
10. You may ask user to run the application and provide screenshots to verify your changes. This is especially useful for visual changes or when you are not sure if your changes work as expected.
11. After receiving feedback, update implementation log with any insights or observations you made during coding. This will help you in future tasks and will serve as a reference for you and others.
12. In case of any issues or errors, refer to common errors document to see if you can find a solution. Search internet to gather more insights. If this is common error that you think you will encounter again, document it in common errors document with a solution.
