sed == stream editor
cli for replacing text

# file.in
Hello, {{NAME}}!
Your ID is {{ID}}.

steps to test this:
1. create file.in
    echo "Hello, {{NAME}}!
    Your ID is {{ID}}." > file.in
2. check contents
    cat file.in
3. use sed to replace placeholders
    sed 's/{{NAME}}/Joe/g; s/{{ID}}/12345/g' file.in > file.out

    sed <sed_syntax> <file_w_placeholder> > <file.out>
    sed_syntax:
    sed/{{NAME}}/Joe/g => replaces all occurrences of {{NAME}} with Joe
    s/{{ID}}/12345/g => replaces all occurrences of {{ID}} with 12345
    s/random/12345/g => replaces all occurrences of random with 12345   # {{PLACE_HOLDER}} is just a convention
4. (optional) can do in-place editing of the file
    sed -i 's/{{NAME}}/Joe/g; s/{{ID}}/12345/g' file.in     # -i replaces the value inside file.in itself
    # NOTE
    for mac u need a backup suffix => a backup file is created with this suffix; its just mac's way to ensure that the of file is preserved
    * using an empty string means u dont want to create a backup; but macos just mandates this...
    sed -i '' 's/{{NAME}}/Joe/g; s/{{ID}}/12345/g' file.in      # no backup created
    sed -i 'bak' 's/{{NAME}}/Joe/g; s/{{ID}}/12345/g' file.in      # no backup with suffix .bak created; file.in.bak