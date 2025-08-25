from talon import Module, actions, registry
import sys, os
import pypandoc
from weasyprint import css




def list_to_markdown_table(file, list_name):
    file.write(f"## {list_name} \n\n")
    command_list = registry.lists[list_name][0].items()
    # file.write(f">\n")
    file.write(f"| command word | {list_name}   |\n")
    file.write("|-----|-----|\n")
    for key, value in command_list:
        file.write("| **" + key + "** | *" + value + "* |\n")

    file.write("\n\n")


def write_alphabet(file):
    list_to_markdown_table(file, "user.letter")


def write_numbers(file):
    list_to_markdown_table(file, "user.number_key")


def write_modifiers(file):
    list_to_markdown_table(file, "user.modifier_key")


def write_special(file):
    list_to_markdown_table(file, "user.special_key")


def write_symbol(file):
    list_to_markdown_table(file, "user.symbol_key")


def write_arrow(file):
    list_to_markdown_table(file, "user.arrow_key")


def write_punctuation(file):
    list_to_markdown_table(file, "user.punctuation")


def write_function(file):
    list_to_markdown_table(file, "user.function_key")


def write_formatters(file):
    file.write(f"## formatters \n\n")
    # command_list = registry.lists['user.formatters'][0].items()
    command_list = {}

    for list_name in registry.lists.keys():
        if "formatter" in str(list_name):
            for k, v in registry.lists[list_name][0].items():
                command_list[k] = v
        else:
            continue  # wrote eighty seven
    print(command_list)

    # command_list = dict(command_list)

    file.write("| command word | user.formatters  |\n")
    file.write("|-----|-----|\n")
    #    file.write("|------|-----|\n")
    for key, value in command_list.items():
        # file.write( "> **"+ key + "** `" + actions.user.formatted_text(f"example of formatting with {key}", value) + "` \n")
        file.write(
            "| **"
            + key
            + "** | "
            + actions.user.formatted_text(f"example of formatting with {key}", value)
            + " | \n"
        )


def write_context_commands(file, commands):
    # write out each command and it's implementation

    for key in commands:
        try:
            rule = commands[key].rule.rule
            implementation = commands[key].target.code.replace("\n", " then, \t\t")
        except Exception:
            continue
        file.write("| **" + rule + "** | *" + implementation + "* |\n")


def pretty_print_context_name(file, name):
    ## The logic here is intended to only print from talon files that have actual voice commands.
    splits = name.split(".")
    index = -1

    os = ""

    if "mac" in name:
        os = "mac"
    if "win" in name:
        os = "win"
    if "linux" in name:
        os = "linux"

    if "talon" in splits[index]:
        index = -2
        short_name = splits[index].replace("_", " ")
    else:
        short_name = splits[index].replace("_", " ")

    if "mac" == short_name or "win" == short_name or "linux" == short_name:
        index = index - 1
        short_name = splits[index].replace("_", " ")

    file.write(f"##  {name}")

    file.write("\n\n\n" + "| command word | " + os + " " + short_name + " |"  + "\n")
    file.write("|----|----|\n")


mod = Module()


@mod.action_class
class user_actions:
    def cheatsheet_md():
        """Print out a sheet of talon commands"""
        # open file

        this_dir = os.path.dirname(os.path.realpath(__file__))
        css_path = os.path.join(this_dir, "cheatsheet.css")
        template_path = os.path.join(this_dir, "template.html")


        chunk_dir_path = os.path.join(this_dir, "cheatsheet-chunked")



        os.makedirs(chunk_dir_path, exist_ok= True)




        chunk_path = os.path.join(chunk_dir_path, "Talon Basic Commands.md")

        chunk = open(chunk_path, "w")

        write_alphabet(chunk)


        write_numbers(chunk)


        write_modifiers(chunk)


        write_special(chunk)


        write_symbol(chunk)


        write_arrow(chunk)


        write_punctuation(chunk)


        write_function(chunk)


        write_formatters(chunk)

        chunk.close()

        # print out all the commands in all of the contexts

        list_of_contexts = registry.contexts.items()

        command_set_dict = {}

        for key, value in list_of_contexts:
            commands = value.commands  # Get all the commands from a context

            if len(commands) > 0:
                command_set= key.split(".")[1]

                if command_set not in list(command_set_dict.keys()):

                    command_set_dict[command_set] = {}
                    command_set_dict[command_set][key] = commands
                else:

                    command_set_dict[command_set][key] = commands


        for (set_name, set) in command_set_dict.items():

            chunk_path = os.path.join(chunk_dir_path, f"{set_name} commands.md")

            chunk = open(chunk_path, "w")

            chunk.write(f"---\ntitle: '{set_name} Command Set' \n\n---\n\n")


            for context, commands in set.items():

                pretty_print_context_name(chunk, context)
                write_context_commands(chunk, commands)

                chunk.write("\n\n")

            chunk.close()


        # for key, value in list_of_contexts:
        #     commands = value.commands  # Get all the commands from a context

        #     if len(commands) > 0:
        #         chunk_path = os.path.join(chunk_dir_path, f"{key.split(".")[1]} Commands.md")


        #         chunk = open(chunk_path, "a")

        #         pretty_print_context_name(chunk, key)
        #         write_context_commands(chunk, commands)

        #         chunk.write("\n\n")

        #         chunk.close()

        cheatsheets = os.listdir(chunk_dir_path)



        for sheet in cheatsheets:

            if sheet.endswith("md"):
                pypandoc.convert_file(os.path.join(chunk_dir_path,sheet), 'html5', format= "markdown-smart", outputfile=os.path.join(chunk_dir_path,f"{sheet.split(".")[0]}.html"), extra_args=[f"--template={template_path}", f"--css={css_path}"])