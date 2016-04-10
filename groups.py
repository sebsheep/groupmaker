#!/usr/bin/python3
from tkinter import *
import json

with open("data.json") as f:
	data = json.loads(f.read())

students = data["students"]
groups = data["groups"]

projects = (
	"Bataille navale",
	"Bomberman",
	"Postit",
	"Ligthsaber",
)

frameworks = ('Node.js', 'Silex')

def write_data(data):
	with open("data.json", "w") as f:
		f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))


def add_group(students_ids, project, framework, workspace=None):
	new_id = str(max(map(int,groups)) + 1)
	group = { "framework": framework, "project": project}
	if workspace:
		group["workspace"] = workspace

	groups[new_id] = group
	for i in students_ids:
		students[i]["group"] = new_id
def nom(student):
	return "%s %s"%(student["nom"], student["prenom"])

def new():
	fen = Tk()
	canvas = Canvas(fen, borderwidth=0, background="#ffffff", height=800)
	frame = Frame(canvas, background="#ffffff")
	vsb = Scrollbar(fen, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=vsb.set)
	vsb.pack(side="right", fill="y")

	canvas.pack(side="left", fill="both", expand=True)
	canvas.create_window((4,4), window=frame, anchor="nw")

	check_vars = [IntVar(fen) for _ in range(len(students))]
	workspace, project, framework = [StringVar(fen) for i in range(3)]
	def action():
		# import ipdb; ipdb.set_trace()
		add_group(
			[i for i, var in enumerate(check_vars) if var.get()],
			project.get(),
			framework.get(),
			workspace.get(),
		)
		write_data(data)
		fen.destroy()
		refresh()
	for student, var in zip(students, check_vars):
		Checkbutton(frame, text=nom(student), variable=var).pack()
	Label(fen, text="Workspace:")
	Entry(fen, textvariable=workspace).pack()
	Frame(fen, height=1, width=50, bg="black").pack()
	for p in projects:
		Radiobutton(fen, text=p, variable=project, value=p).pack(anchor=W)
	Frame(fen, height=1, width=50, bg="black").pack()
	for f in frameworks:
		Radiobutton(fen, text=f, variable=framework, value=f).pack(anchor=W)
	Button(fen, text="Créer !", command=action).pack()
	

def refresh():
	for widget in main_window.winfo_children():
		widget.destroy()
	for i, group in sorted(groups.items(), key=lambda x: int(x[0])):
		Message(main_window, text="Groupe {i} sur {project} avec {framework} à {workspace}: {students}.".format(**{
			"i": i, 
			"project": group.get("project", "NON DEF"),
			"framework": group.get("framework", "NON DEF"),
			"workspace": group.get("workspace", "NON DEF"), 
			"students": ",".join(nom(s) for s in students if s["group"] == i),
		})).pack()
		Frame(main_window, height=1, width=50, bg="black").pack()
	Button(main_window, text="Nouveau groupe", command=new).pack()

if __name__ == '__main__':
	main_window = Tk()
	refresh()
	
	
	
	mainloop()