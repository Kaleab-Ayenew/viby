class Command{
    command string
}




function GenerateCommand(terminal_history: string, user_input: string) -> Command{
  // see ollama-clients.baml
  client Gemma3n
  // client Mistral
  // client Gemma2
  // client Phi3

  // The prompt uses Jinja syntax. Change the models or this text and watch the prompt preview change!
  prompt #"
    Examine any provided terminal history and the user's request, then output a shell command according to the following schema.

    Terminal History:
    ---
    {{ terminal_history }}
    ---

    User Input:
    ---
    {{ user_input }}
    ---

    {# special macro to print the output instructions. #}
    {{ ctx.output_format }}

    JSON:
  "#
}

test OllamaTest1 {
  functions [GenerateCommand]
  args {
    terminal_history #"
Script started on 2025-07-07 16:43:07+03:00 [TERM="xterm-256color" TTY="/dev/pts/11" COLUMNS="112" LINES="11"]
kalish@pop-os:~/Documents/projects/terminal_assistant$ git push
To https://github.com/Kaleab-Ayenew/vity
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/Kaleab-Ayenew/vity'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
kalish@pop-os:~/Documents/projects/terminal_assistant$ git pull
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge (the default strategy)
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
kalish@pop-os:~/Documents/projects/terminal_assistant$ vity chat what does this mean
🤖 Vity is thinking...
The messages you see when you try to `git push` and then `git pull` indicate that your local branch and the remote branch have diverged. Here's a breakdown:

1. **git push rejected (non-fast-forward)**:
   - This means your local branch is behind the remote branch.
   - Someone else (or you from another machine) has pushed changes to the remote branch that you don't have locally.
   - Git prevents you from pushing because it would overwrite those changes.

2. **git pull hint about divergent branches**:
   - When you try to pull, Git notices that your local branch and the remote branch have diverged (both have unique commits).
   - Git needs to know how to reconcile these differences.
   - It asks you to specify a strategy for merging the changes:
     - `git config pull.rebase false` to merge (default)
     - `git config pull.rebase true` to rebase
     - `git config pull.ff only` to only allow fast-forward merges

3. **What you should do**:
   - Decide how you want to integrate the remote changes:
     - If you want to merge the remote changes into your local branch, run:
       ```
       git pull --no-rebase
       ```
     - If you want to rebase your changes on top of the remote branch, run:
       ```
       git pull --rebase
       ```
   - Alternatively, set a default behavior globally, for example:
     ```
     git config --global pull.rebase false
     ```
     or
     ```
     git config --global pull.rebase true
     ```
   - After successfully pulling and resolving any conflicts, you can push your changes again.

In summary, Git is telling you that your local and remote branches have different commits, and you need to specify how to combine them before pushing.
kalish@pop-os:~/Documents/projects/terminal_assistant$ vity status
🔴 Recording active:
  📝 Terminal log: /home/kalish/.local/share/vity/logs/20250707-164307-229354.log
  💬 Chat history: /home/kalish/.local/share/vity/chat/20250707-164307-229354.json
kalish@pop-os:~/Documents/projects/terminal_assistant$ git pull --rebase
Successfully rebased and updated refs/heads/main.
kalish@pop-os:~/Documents/projects/terminal_assistant$ git push
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 12 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (6/6), 1.01 KiB | 1.01 MiB/s, done.
Total 6 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/Kaleab-Ayenew/vity
   8911aa0..53fe21f  main -> main
kalish@pop-os:~/Documents/projects/terminal_assistant$ git tag
v0.1.0
v0.1.1
v0.1.2
v0.1.3
v0.1.5
v0.1.6
v0.1.8
kalish@pop-os:~/Documents/projects/terminal_assistant$ source .venv/bin/activate
    "#
    user_input #"
    list all services running on port 80
    "#
  }
}