from lark import Lark

# Step 1: Read the grammar from a text file
with open("oml3_lark.txt", "r") as file:
    grammar = file.read()

# Step 2: Create the Lark parser using the grammar
parser = Lark(grammar)

# Step 3: Define a function to parse input
def parse_input(input_str):
    parse_tree = parser.parse(input_str)
    return parse_tree.pretty()

# Step 4: Test the parser with an example input
input_str = """vocabulary <http://example.com/tutorial1/vocabulary/pizza#> as pizza {

    extends <http://www.w3.org/2001/XMLSchema#> as xsd

    extends <http://purl.org/dc/elements/1.1/> as dc

    extends <http://www.w3.org/2000/01/rdf-schema#> as rdfs


    @rdfs:comment "The class of things that are uniquely identified by id"
    aspect IdentifiedThing [
        key hasId
    ]

    @rdfs:comment "The id property of an identified thing"
    scalar property hasId [
        domain IdentifiedThing
        range xsd:string
        functional
    ]

    // Identified Things

    @rdfs:comment "The class of food items"
    concept Food < IdentifiedThing

    @rdfs:comment "A relation from a food to another used as an ingredient"
    relation entity HasIngredient [
        from Food
        to Food
        forward hasIngredient
        reverse isIngredientOf
        transitive
    ]

    @rdfs:comment "An enumeration of spiciness levels"
    scalar Spiciness [
        oneOf "Hot", "Medium", "Mild"
    ]

    @rdfs:comment "The spiciness property of a food item"
    scalar property hasSpiceness [
        domain Food
        range Spiciness
        functional
    ]

    // Foods

    @rdfs:comment "The class of pizzas"
    concept Pizza < Food [
        restricts some hasBase to PizzaBase
    ]

    @rdfs:comment "The class of pizza bases"
    concept PizzaBase < Food

    @rdfs:comment "The class of pizza toppings"
    concept PizzaTopping < Food

    @rdfs:comment "A relation from a pizza to a base"
    relation entity HasBase [
        from Pizza
        to PizzaBase
        forward hasBase
        reverse isBaseOf
        functional
        inverse functional
    ] < HasIngredient

    @rdfs:comment "A relation from a pizza to a topping"
    relation entity HasTopping [
        from Pizza
        to PizzaTopping
        forward hasTopping
        reverse isToppingOf
        inverse functional
    ] < HasIngredient

    // Pizzas

    @rdfs:comment "The class of pizzas with some cheese toppings"
    concept CheesyPizza < Pizza [
        restricts some hasTopping to CheeseTopping
    ]

    @rdfs:comment "The class of pizzas with some meat toppings"
    concept MeatyPizza < Pizza [
        restricts some hasTopping to MeatTopping
    ]

    @rdfs:comment "The class of pizzas with all vegetarian toppings"
    concept VegetarianPizza < Pizza [
        restricts all hasTopping to VegetarianTopping
    ]

    @rdfs:comment "The class of American pizzas"
    concept American < CheesyPizza, MeatyPizza [
        restricts some hasTopping to MozzarellaTopping
        restricts some hasTopping to SausageTopping
        restricts some hasTopping to TomatoTopping
    ]

    @rdfs:comment "The class of Veneziana pizzas"
    concept Veneziana < CheesyPizza, MeatyPizza [
        restricts some hasTopping to MozzarellaTopping
        restricts some hasTopping to TomatoTopping
        restricts some hasTopping to SultanaTopping
    ]

    @rdfs:comment "The class of Margherita pizzas"
    concept Margherita < CheesyPizza, VegetarianPizza [
        restricts some hasTopping to MozzarellaTopping
        restricts some hasTopping to TomatoTopping
    ]

    // Pizza Bases

    @rdfs:comment "The class of deep pan bases"
    concept DeepPanBase < PizzaBase

    @rdfs:comment "The class of thin and crispy bases"
    concept ThinAndCrispyBase < PizzaBase

    // Pizza Toppings

    @rdfs:comment "The class of meat toppings"
    concept MeatTopping < PizzaTopping

    @rdfs:comment "The class of vegetarian toppings"
    concept VegetarianTopping < PizzaTopping

    @rdfs:comment "The class of hot spiciness toppings"
    concept HotTopping < PizzaTopping [
        restricts hasSpiceness to "Hot"
    ]

    @rdfs:comment "The class of medium spiciness toppings"
    concept MediumTopping < PizzaTopping [
        restricts hasSpiceness to "Medium"
    ]

    @rdfs:comment "The class of mild spiciness toppings"
    concept MildTopping < PizzaTopping [
        restricts hasSpiceness to "Mild"
    ]

    // Meat Topping

    @rdfs:comment "The class sausage toppings"
    concept SausageTopping < MeatTopping, MildTopping
    @rdfs:comment "The class spiced beef toppings"
    concept SpicedBeefTopping < MeatTopping, HotTopping

    // Vegetarion Toppings

    @rdfs:comment "The class sauce toppings"
    concept SauceTopping < VegetarianTopping
    @rdfs:comment "The class cheese toppings"
    concept CheeseTopping < VegetarianTopping
    @rdfs:comment "The class fruit toppings"
    concept FruitTopping < VegetarianTopping
    @rdfs:comment "The class vegetable toppings"
    concept VegetableTopping < VegetarianTopping

    // Sauce Toppings

    @rdfs:comment "The class of tabasco toppings"
    concept TobascoTopping < SauceTopping, HotTopping

    // Cheese Toppings

    @rdfs:comment "The class of parmesan toppings"
    concept ParmesanTopping < CheeseTopping, MildTopping
    @rdfs:comment "The class of mozzarella toppings"
    concept MozzarellaTopping < CheeseTopping, MildTopping

    // Fruit Toppings

    @rdfs:comment "The class of sultana toppings"
    concept SultanaTopping < FruitTopping, MediumTopping

    // Vegetable Toppings

    @rdfs:comment "The class of pepper toppings"
    concept PepperTopping < VegetableTopping
    @rdfs:comment "The class of tomatoe toppings"
    concept TomatoTopping < VegetableTopping, MildTopping

    // Pepper Toppings

    @rdfs:comment "The class of jalapeno pepper toppings"
    concept JalapenoPepperTopping < PepperTopping, HotTopping
    @rdfs:comment "The class of sweet pepper toppings"
    concept SweetPepperTopping < PepperTopping, MildTopping
}
"""

# Parse the input and print the result
try:
    parsed_result = parse_input(input_str)
    print(parsed_result)
except Exception as e:
    print(f"Error: {e}")

# Step 4: Test the parser with an example input
input_str = """@dc:creator "SIE Disruption Lab"
@dc:contributor "Joe Gregory"
@dc:description "A vocabulary to capture the foundation terminology required by the SIE Disruption Lab. Note that this is essentially a simplified version of gUFO."
@dc:hasVersion "0.1"
vocabulary <http://uaontologies.com/UA_Foundation/UA_Foundation#> as foundation {

	////////////////////////////////////////////////////////////////////////////////////

	/////// Vocabulary Imports ///////


	// Import standard vocabularies

    extends <http://purl.org/dc/elements/1.1/> as dc
    extends <http://www.w3.org/2000/01/rdf-schema#> as rdfs
    extends <http://www.w3.org/2001/XMLSchema#> as xsd


	///////////////////////////////////////////////////////////////////////////////////

	/////// Vocabulary Definitions ///////


	///// Aspects

	@rdfs:label "Contained Element"
	aspect ContainedElement

	@rdfs:label "Container"
	aspect Container

	@rdfs:label "SDC Carrier"
	aspect SDCCarrier

	@rdfs:label "GDC Carrier"
	aspect GDCCarrier


	///// Concepts

	@rdfs:label "IdentifiedEntity"
	concept IdentifiedEntity

	@rdfs:label "Occurrent"
	concept Occurrent < IdentifiedEntity, Container, ContainedElement, GDCCarrier, SDCCarrier [
		restricts all contains to Occurrent
		restricts all isContainedIn to Occurrent
	]

	@rdfs:label "Continuant"
	concept Continuant < IdentifiedEntity

	@rdfs:label "Temporal Region"
	concept TemporalRegion < Occurrent, Container, ContainedElement [
		restricts all contains to TemporalRegion
		restricts all isContainedIn to TemporalRegion
	]

	@rdfs:label "Process"
	concept Process < Occurrent, Container, ContainedElement, SDCCarrier [
		restricts all contains to Process
		restricts all isContainedIn to Process
	]

	@rdfs:label "Independent Continuant"
	concept IndependentContinuant < Continuant, SDCCarrier, GDCCarrier

	@rdfs:label "Specifically Dependent Continuant"
	concept SpecificallyDependentContinuant < Continuant, SDCCarrier, GDCCarrier [
		restricts some specificallyDependentOn to SDCCarrier
	]

	@rdfs:label "Generically Dependent Continuant"
	concept GenericallyDependentContinuant < Continuant

	@rdfs:label "Realizable Entity"
	concept RealizableEntity < SpecificallyDependentContinuant

	@rdfs:label "Quality"
	concept Quality < SpecificallyDependentContinuant

	@rdfs:label "Disposition"
	concept Disposition < RealizableEntity

	@rdfs:label "Function"
	concept Function < Disposition, Container, ContainedElement [
		restricts all contains to Function
		restricts all isContainedIn to Function
	]

	@rdfs:label "Material Entity"
	concept MaterialEntity < IndependentContinuant, ContainedElement

	@rdfs:label "Object Aggregate"
	concept ObjectAggregate < MaterialEntity, Container [
		restricts all contains to MaterialEntity
		restricts all isContainedIn to ObjectAggregate
	]

	@rdfs:label "Object"
	concept Object < MaterialEntity

	@rdfs:label "Immaterial Entity"
	concept ImmaterialEntity < IndependentContinuant

	@rdfs:label "Site"
	concept Site < ImmaterialEntity

	@rdfs:label "Energy"
	concept Energy < ImmaterialEntity

	@rdfs:label "Role"
	concept Role < GenericallyDependentContinuant, Container, ContainedElement, SDCCarrier [
		restricts all contains to Role
		restricts all isContainedIn to Role
	]



	///// Relations

	@rdfs:label "Contains"
	@dc:description "[=Contains=] is a..."
	relation entity Contains [
		from Container
		to ContainedElement
		@rdfs:label "contains"
		forward contains
		@rdfs:label "is contained in"
		reverse isContainedIn
		asymmetric
		irreflexive
	]

	@rdfs:label "Specifically Dependent On"
	@dc:description "[=SpecificallyDependentOn=] is a..."
	relation entity SpecificallyDependentOn [
		from SpecificallyDependentContinuant
		to SDCCarrier
		@rdfs:label "specifically dependent on"
		forward specificallyDependentOn
		@rdfs:label "has specific dependent"
		reverse hasSpecificDependent
		asymmetric
		irreflexive
	]

	@rdfs:label "Generically Dependent On"
	@dc:description "[=GenericallyDependentOn=] is a..."
	relation entity GenericallyDependentOn [
		from GenericallyDependentContinuant
		to GDCCarrier
		@rdfs:label "generically dependent on"
		forward genericallyDependentOn
		@rdfs:label "has generic dependent"
		reverse hasGenericDependent
		asymmetric
		irreflexive
	]

	@rdfs:label "Occupies"
	@dc:description "[=Occupies=] is a..."
	relation entity Occupies [
		from MaterialEntity
		to Site
		@rdfs:label "occupies"
		forward occupies
		@rdfs:label "is occupied by"
		reverse isOccupiedBy
		asymmetric
		irreflexive
	]



	///// Scalar Properties

	@rdfs:label "has name"
	@dc:description "[=hasName=] is a FOUNDATIONAL scalar property - all entities can have a name"
	scalar property hasName [
		domain IdentifiedEntity
		range xsd:string
	]

	@rdfs:label "has ID"
	@dc:description "[=hasID=] is a FOUNDATIONAL scalar property - all entities can have an ID"
	scalar property hasID [
		domain IdentifiedEntity
		range xsd:string
	]

	@rdfs:label "has natural language description"
	@dc:description "[=hasNaturalLanguageDescription=] is a FOUNDATIONAL scalar property - all entities can have a natural language description"
	scalar property hasNaturalLanguageDescription [
		domain IdentifiedEntity
		range xsd:string
	]

	@rdfs:label "has begin instant"
	@dc:description "[=hasBeginInstant=] ..."
	scalar property hasBeginInstant [
		domain TemporalRegion
		range xsd:dateTime
	]

	@rdfs:label "has end instant"
	@dc:description "[=hasEndInstant=] ..."
	scalar property hasEndInstant [
		domain TemporalRegion
		range xsd:dateTime
	]

	///// Rules
	}
"""

# Parse the input and print the result
try:
    parsed_result = parse_input(input_str)
    print(parsed_result)
except Exception as e:
    print(f"Error: {e}")

# Step 4: Test the parser with an example input
input_str = """@dc:creator "SIE Disruption Lab"
@dc:contributor "Joe Gregory"
@dc:description "A vocabulary to capture the organization patterns required by the SIE Disruption Lab."
@dc:hasVersion "0.1"
vocabulary <http://uaontologies.com/UA_Core/UA_Agent#> as UA_Agent {

	////////////////////////////////////////////////////////////////////////////////////

	/////// Vocabulary Imports ///////


	// Import standard vocabularies

    extends <http://purl.org/dc/elements/1.1/> as dc
    extends <http://www.w3.org/2000/01/rdf-schema#> as rdfs
    //extends <http://www.w3.org/2001/XMLSchema#> as xsd

    // Import relevant vocabularies

    extends <http://uaontologies.com/UA_Foundation/UA_Foundation#> as foundation

	extends <http://uaontologies.com/UA_Core/UA_Information#> as info
	//extends <http://uaontologies.com/UA_Core/UA_Event#> as event


	///////////////////////////////////////////////////////////////////////////////////

	/////// Vocabulary Definitions ///////

	///// Aspects

	@rdfs:label "Producer"
	@dc:description "A [=Producer=] is a ..."
	aspect Producer

	@rdfs:label "Consumer"
	@dc:description "A [=Consumer=] is a ..."
	aspect Consumer

	@rdfs:label "Agent"
	@dc:description "An [=Agent=]..."
	aspect Agent < foundation:SDCCarrier



	///// Concepts

	@rdfs:label "Organization"
	@dc:description "A [=Organization=]..."
	concept Organization < Agent, foundation:MaterialEntity, foundation:Container, foundation:ContainedElement [
		restricts all foundation:contains to Organization
		restricts all foundation:isContainedIn to Organization
	]

	@rdfs:label "Person"
	@dc:description "A [=Person=]..."
	concept Person < Agent, foundation:MaterialEntity

	@rdfs:label "ProcessOwner"
	@dc:description "A [=ProcessOwner=] is a ..."
	concept ProcessOwner < foundation:Role

	@rdfs:label "Managed Process"
	@dc:description "A [=ManagedProcess=]..."
	concept ManagedProcess < foundation:Process

	@rdfs:label "Procedure"
	@dc:description "A [=Procedure=]..."
	concept Procedure < info:PrescriptiveInformationEntity [
		restricts all info:prescribes to foundation:Process
		restricts some info:prescribes to foundation:Process
	]

	@rdfs:label "Plan"
	@dc:description "A [=Plan=]..."
	concept Plan < info:PrescriptiveInformationEntity [
		restricts all info:prescribes to foundation:Process
		restricts some info:prescribes to foundation:Process
		restricts some foundation:contains to Procedure
	]



	///// Relations

	@rdfs:label "Belongs To"
	@dc:description "[=BelongsTo=] is a..."
	relation entity BelongsTo [
		from Person
		to Organization
		@rdfs:label "belongs to"
		forward belongsTo
		@rdfs:label "has belonging"
		reverse hasBelonging
		asymmetric
		irreflexive
	]

	@rdfs:label "Responsible For"
	@dc:description "[=ResponsibleFor=] is a..."
	relation entity ResponsibleFor [
		from ProcessOwner
		to ManagedProcess
		@rdfs:label "responsible for"
		forward responsibleFor
		@rdfs:label "is responsibility of"
		reverse isResponsibilityOf
		asymmetric
		irreflexive
	]

	@rdfs:label "Has Input"
	@dc:description "[=HasInput=] is a..."
	relation entity HasInput [
		from Consumer
		to foundation:Continuant
		@rdfs:label "has input"
		forward hasInput
		@rdfs:label "is input of"
		reverse isInputOf
		asymmetric
		irreflexive
	]

	@rdfs:label "Has Output"
	@dc:description "[=HasOutput=] is a..."
	relation entity HasOutput [
		from Producer
		to foundation:Continuant
		@rdfs:label "has output"
		forward hasOutput
		@rdfs:label "is output of"
		reverse isOutputOf
		asymmetric
		irreflexive
	]

	@rdfs:label "Is Role Of"
	@dc:description "[=IsRoleOf=] is a..."
	relation entity IsRoleOf [
		from foundation:Role
		to Agent
		@rdfs:label "is role of"
		forward isRoleOf
		@rdfs:label "has role"
		reverse hasRole
		asymmetric
		irreflexive
	]
	< foundation:GenericallyDependentOn

	@rdfs:label "Has Organizational Context"
	@dc:description "[=HasOrganizationContext=] is a "
	relation entity HasOrganizationalContext [
		from foundation:Role
		to Organization
		@rdfs:label "has organizational context"
		forward hasOrganziationalContext
		@rdfs:label "is organizational context of"
		reverse isOrganizationalContextOf
		asymmetric
		irreflexive
	]

	@rdfs:label "Has Planned Temporal Region"
	@dc:description "[=HasPlannedTemporalRegion=] is a "
	relation entity HasPlannedTemporalRegion [
		from Plan
		to foundation:TemporalRegion
		@rdfs:label "has planned temporal region"
		forward hasPlannedTemporalRegion
		@rdfs:label "is planned temporal region of"
		reverse isPlannedTemporalRegionOf
		asymmetric
		irreflexive
	]



	///// Scalar Properties



	///// Redefined Concepts

	ref concept foundation:Process < Producer, Consumer




	///// Rules


}
"""

# Parse the input and print the result
try:
    parsed_result = parse_input(input_str)
    print(parsed_result)
except Exception as e:
    print(f"Error: {e}")

# Function to visualize the parse tree
def visualize_parse_tree(parse_tree):
    def build_graph(tree, graph=None):
        if graph is None:
            graph = Digraph()
        if isinstance(tree, Tree):
            graph.node(tree.data)
            for child in tree.children:
                build_graph(child, graph)
                graph.edge(tree.data, str(child))
        else:
            # For Token, just use its value
            graph.node(str(tree))
        return graph

    graph = build_graph(parse_tree)
    return graph

# Visualize the parse tree
graph = visualize_parse_tree(parsed_result)
graph.render("pizza_tree", format="png", view=True)
