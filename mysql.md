1. Get all statuses, not repeating, alphabetically ordered.

```
SELECT DISTINCT tasks.status
 from tasks
 order by tasks.status ASC;
```

2. Get the count of all tasks in each project, order by task count desc

```
SELECT project_id, COUNT(project_id) as task_count
 from tasks
 group by project_id
 order by task_count DESC;
```

3. Get the count of all tasks in each project, order by project names. 

!!!May be a good option to consider left join!!!

```
SELECT project_id, COUNT(project_id) as task_count
 from tasks
 inner join projects
 on tasks.project_id = projects.id
 group by project_id;
```

4. Get the tasks for all projects having the name starting with "N" letter.

```
SELECT tasks.name from tasks
 inner join projects
 on tasks.project_id = projects.id
 where projects.name like 'N%';
```

5. 



6. Get the list of tasks with duplicate names, order alphabetically.

```
SELECT tasks.name, Count(tasks.name) as counter from tasks 
 group by tasks.name
 having counter > 1
 order by tasks.name ASC;
```

