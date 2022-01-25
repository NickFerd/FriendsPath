# Friends Path

Friends Paths is a script that finds and builds a path of friends between two people.
Script uses breadth-first search algorithm and makes calls via VK_API.

Program work and output result demonstration.
```
100%|██████████| 399/399 [00:00<00:00, 400557.04it/s]
100%|██████████| 631/631 [00:00<00:00, 633007.85it/s]
15 - Access denied: user deactivated, User ID - 6246212
15 - Access denied: user deactivated, User ID - 6285355
100%|██████████| 1620/1620 [00:00<00:00, 811413.00it/s]
100%|██████████| 651/651 [00:00<00:00, 650271.95it/s]
100%|██████████| 680/680 [00:00<00:00, 712497.31it/s]
100%|██████████| 256/256 [00:00<00:00, 256691.81it/s]
100%|██████████| 215/215 [00:00<?, ?it/s]
100%|██████████| 129/129 [00:00<?, ?it/s]
100%|██████████| 916/916 [00:00<00:00, 916503.45it/s]
100%|██████████| 52/52 [00:00<00:00, 52115.61it/s]
100%|██████████| 277/277 [00:00<00:00, 278214.13it/s]
30 - This profile is private, User ID - 12656409
100%|██████████| 66/66 [00:00<?, ?it/s]
100%|██████████| 84/84 [00:00<00:00, 84247.14it/s]
1. Nikita Ferdman
https://vk.com/id20067703

2. Alexey Axenov
https://vk.com/id13120790

3. Ivan Zhdanov
https://vk.com/id191277999

You are 2 handshakes away from this person!

```
- Each progress bar shows search through friends of a certain user.
- If an error occurs while getting friends of a user, the program prints out error's code, message and the user ID.
- The result output includes full name of a person and a link to his/her VK page.
