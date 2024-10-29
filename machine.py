import dataclasses


@dataclasses.dataclass
class Machine:
	name:str=""
	source:str=""
	description:str=""
	year:str=""
	manufacturer:str=""
	parent:str=""
	category:str=""

	@classmethod
	def fields(cls:type["Machine"])->list:
		return [x.name for x in list(dataclasses.fields(Machine))]
