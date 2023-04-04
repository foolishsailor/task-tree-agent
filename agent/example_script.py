import os
import sys
import pickle
from action_interface import ActionInterface
from agent_class import Agent

# add paths to action sets
sys.path.append(os.path.join(os.path.dirname(__file__), "../action_sets/task_tree"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../action_sets/long_form_writing"))

from task_tree_management import task_tree_management_action_set
from SDF import Document
from writing_action_set import writing_action_set


task_description = "Write a long-form essay about the history of technology's impact on society."

human_notes = """
It should be written for a sophisticated audience.

Let's include lots of specific examples in this essay, so the reader feels like they're constantly learning new things. The specific examples should tie into the main thesis of the essay though.

This essay should be written in the style of a best-selling non-fiction author like Walter Isaacson or Malcolm Gladwell.

The essay should be about 10,000 words long. It should be broken up into 4-6 sections.
""".strip()

file_name = "technology_and_society.pkl"
model_name = "gpt-4" # "gpt-3.5-turbo"
pick_up_where_we_left_off = False

def main():
    if pick_up_where_we_left_off:
        with open(file_name, "rb") as f:
            agent = pickle.load(f)

        # Update the action interface to reflect changes made in the action sets
        agent.action_interface = ActionInterface(
            action_sets=[task_tree_management_action_set, writing_action_set],
            task_tree=agent.task_tree,
            sdf_document=agent.sdf_document,
        )
    else:
        # Create an agent with an initial task description
        agent = Agent(
            task_description=task_description,
            action_sets=[task_tree_management_action_set, writing_action_set],
            sdf_document=Document(title="Untitled", human_notes=human_notes, section_type="Section", model_name=model_name),
            save_path=file_name,
        )

    # Run the agent for a specified number of iterations
    agent.run(max_iterations=100, model_name=model_name, verbose=True)

    # Print the final task tree
    print("\nFinal Task Tree:")
    agent.task_tree.print_tree()

    # Print the final SDF document
    print("\nFinal SDF Document:")
    agent.sdf_document.display()


if __name__ == "__main__":
    main()