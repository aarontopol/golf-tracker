#!/usr/bin/env python3
"""Generate crossword puzzles for the crossword app.

Builds 100 easy and 100 medium criss-cross style crosswords from curated
word/clue banks, verifies every puzzle (interlocking, connected, consistent
crossings), and writes crossword/puzzles.js consumed by the app.
"""
import json
import random
import sys

# ---------------------------------------------------------------------------
# Word banks: (WORD, clue). Topics are deliberately all over the map.
# ---------------------------------------------------------------------------

EASY = [
    ("CAT", "Whiskered pet that purrs"),
    ("DOG", "Man's best friend"),
    ("SUN", "Star at the center of our solar system"),
    ("MOON", "It causes ocean tides"),
    ("STAR", "Twinkler in the night sky"),
    ("TREE", "Oak or maple, for example"),
    ("FISH", "Goldfish or tuna"),
    ("BIRD", "Robin or blue jay"),
    ("CAKE", "Birthday dessert with candles"),
    ("MILK", "Classic cookie dunker"),
    ("BOOK", "It has chapters and pages"),
    ("RAIN", "Umbrella weather"),
    ("SNOW", "White winter flakes"),
    ("WIND", "It fills a sailboat's sails"),
    ("FIRE", "Campers roast marshmallows over it"),
    ("LAKE", "Body of water smaller than a sea"),
    ("SHIP", "Ocean-going vessel"),
    ("KING", "Chess piece you must protect"),
    ("QUEEN", "Most powerful chess piece"),
    ("FROG", "Green hopper that says ribbit"),
    ("BEAR", "Animal that hibernates in winter"),
    ("LION", "King of the jungle"),
    ("TIGER", "Big cat with stripes"),
    ("ZEBRA", "Striped African animal"),
    ("HORSE", "Animal that gallops"),
    ("SHEEP", "Wool provider"),
    ("GOAT", "Farm animal, or Greatest Of All Time"),
    ("DUCK", "Quacking pond bird"),
    ("OWL", "Bird that hoots at night"),
    ("BEE", "Honey maker"),
    ("ANT", "Tiny picnic invader"),
    ("FOX", "Sly woodland animal"),
    ("WOLF", "Animal that howls at the moon"),
    ("DEER", "Bambi, for one"),
    ("CRAB", "Beach animal that walks sideways"),
    ("SEAL", "Whiskered swimmer that barks"),
    ("WHALE", "Largest animal on Earth"),
    ("SHARK", "Ocean predator with fins"),
    ("SNAKE", "Reptile with no legs"),
    ("MOUSE", "Cheese-loving rodent, or computer clicker"),
    ("PIZZA", "Pie with cheese and pepperoni"),
    ("TACO", "Folded tortilla treat"),
    ("SOUP", "Chicken noodle, for one"),
    ("BREAD", "Loaf from the bakery"),
    ("APPLE", "Fruit that keeps the doctor away"),
    ("GRAPE", "Small fruit that grows in bunches"),
    ("LEMON", "Sour yellow fruit"),
    ("MANGO", "Sweet tropical fruit"),
    ("PEACH", "Fuzzy orchard fruit"),
    ("PEAR", "Fruit shaped like a lightbulb"),
    ("PLUM", "Purple stone fruit"),
    ("CORN", "Vegetable on a cob"),
    ("BEAN", "Chili ingredient"),
    ("RICE", "Grain served with stir-fry"),
    ("EGG", "Breakfast food you can scramble"),
    ("HAM", "Meat in a classic sandwich"),
    ("PIE", "Dessert with a crust"),
    ("JAM", "Sweet spread for toast"),
    ("TEA", "Drink brewed in a kettle"),
    ("SODA", "Fizzy soft drink"),
    ("JUICE", "Orange breakfast drink"),
    ("HONEY", "Sweet stuff bees make"),
    ("SUGAR", "Sweetener in cookies"),
    ("SALT", "Pepper's shaker partner"),
    ("CHIP", "Salsa scooper"),
    ("NUT", "Squirrel's snack"),
    ("PARIS", "City with the Eiffel Tower"),
    ("ROME", "City with the Colosseum"),
    ("EGYPT", "Land of the pyramids"),
    ("CHINA", "Country with the Great Wall"),
    ("SPAIN", "Country famous for flamenco"),
    ("INDIA", "Country of the Taj Mahal"),
    ("TEXAS", "The Lone Star State"),
    ("OCEAN", "The Pacific, for example"),
    ("BEACH", "Sandy shore for sunbathing"),
    ("RIVER", "The Nile or the Amazon"),
    ("HILL", "Small mountain"),
    ("CAVE", "Bat's dark home"),
    ("DESERT", "The Sahara, for one"),
    ("ISLAND", "Land surrounded by water"),
    ("MAP", "Treasure hunter's guide"),
    ("SOCCER", "Sport with a World Cup"),
    ("TENNIS", "Sport played at Wimbledon"),
    ("GOLF", "Sport with birdies and bogeys"),
    ("HOCKEY", "Sport played with a puck"),
    ("SKI", "Glide down a snowy slope"),
    ("SWIM", "Move through water"),
    ("RACE", "Contest of speed"),
    ("TEAM", "Group of players"),
    ("GOAL", "Score in soccer"),
    ("BAT", "Baseball hitter's tool, or cave flier"),
    ("BALL", "Round object for many sports"),
    ("PIANO", "Instrument with 88 keys"),
    ("DRUM", "Instrument you beat"),
    ("FLUTE", "Woodwind you blow across"),
    ("VIOLIN", "String instrument with a bow"),
    ("SONG", "Tune with lyrics"),
    ("DANCE", "Move to the music"),
    ("MOVIE", "Film at the theater"),
    ("ACTOR", "Star of a film"),
    ("ROBOT", "Mechanical helper"),
    ("MAGIC", "A wizard's specialty"),
    ("CLOWN", "Circus funnyman"),
    ("TENT", "Camper's shelter"),
    ("KITE", "Toy that flies on a string"),
    ("CHESS", "Game with rooks and knights"),
    ("CARD", "Ace or king, e.g."),
    ("DICE", "Cubes rolled in board games"),
    ("PUZZLE", "Jigsaw or crossword"),
    ("TRAIN", "It runs on rails"),
    ("PLANE", "It has wings and a pilot"),
    ("BOAT", "Rowed or sailed craft"),
    ("TRUCK", "Big rig on the highway"),
    ("WHEEL", "Round part of a car"),
    ("ROAD", "Cars travel on it"),
    ("HOUSE", "Place to call home"),
    ("DOOR", "You knock on it"),
    ("WINDOW", "Glass pane you look through"),
    ("CHAIR", "Seat with four legs"),
    ("TABLE", "Furniture you dine at"),
    ("BED", "Where you sleep"),
    ("LAMP", "It lights up a room"),
    ("CLOCK", "It tells the time"),
    ("PHONE", "Device for calls and texts"),
    ("RADIO", "You tune in to it"),
    ("CAMERA", "It takes photos"),
    ("BRUSH", "Painter's tool"),
    ("PENCIL", "Writing tool with an eraser"),
    ("PAPER", "You write on it"),
    ("SCHOOL", "Place with teachers and desks"),
    ("MATH", "Subject with numbers"),
    ("MUSIC", "Art of sound"),
    ("PAINT", "Artist's colorful medium"),
    ("COLOR", "Red, blue, or green"),
    ("GREEN", "Color of grass"),
    ("BLUE", "Color of a clear sky"),
    ("RED", "Color of a stop sign"),
    ("PINK", "Color of flamingos"),
    ("GOLD", "Color of first-place medals"),
    ("SILVER", "Second-place medal metal"),
    ("SHOE", "Footwear with laces"),
    ("SOCK", "It goes on before a shoe"),
    ("HAT", "Head topper"),
    ("COAT", "Winter outerwear"),
    ("GLOVE", "Hand warmer"),
    ("SCARF", "Neck warmer"),
    ("RING", "Jewelry for a finger"),
    ("CROWN", "Royal headwear"),
    ("SMILE", "Happy expression"),
    ("LAUGH", "React to a good joke"),
    ("SLEEP", "What you do at night"),
    ("DREAM", "Nighttime story in your head"),
    ("HEART", "It pumps blood"),
    ("HAND", "It has five fingers"),
    ("FOOT", "It has five toes"),
    ("NOSE", "Smelling organ"),
    ("EAR", "Hearing organ"),
    ("EYE", "Seeing organ"),
    ("HAIR", "It grows on your head"),
    ("TOOTH", "Dentist's concern"),
    ("DOCTOR", "Person who treats patients"),
    ("NURSE", "Hospital caregiver"),
    ("CHEF", "Restaurant cook"),
    ("FARMER", "Person who grows crops"),
    ("PILOT", "Person who flies planes"),
    ("BAKER", "Person who makes bread"),
    ("ARTIST", "Person who paints or sculpts"),
    ("SPY", "Secret agent"),
    ("PIRATE", "Sailor with a treasure map"),
    ("KNIGHT", "Armored horseman of old"),
    ("WIZARD", "Spell caster with a wand"),
    ("GIANT", "Huge fairy-tale figure"),
    ("FAIRY", "Tiny winged magical being"),
    ("DRAGON", "Fire-breathing beast of legend"),
    ("GHOST", "Halloween spirit that says boo"),
    ("WITCH", "Broomstick rider"),
    ("SPACE", "Where astronauts go"),
    ("ROCKET", "It blasts off"),
    ("PLANET", "Mars or Venus"),
    ("EARTH", "Our home planet"),
    ("MARS", "The Red Planet"),
    ("COMET", "Icy space object with a tail"),
    ("CLOUD", "Fluffy thing in the sky"),
    ("STORM", "Thunder and lightning event"),
    ("SPRING", "Season of blooming flowers"),
    ("SUMMER", "Hottest season"),
    ("WINTER", "Coldest season"),
    ("FALL", "Season of dropping leaves"),
    ("LEAF", "It falls from a tree in autumn"),
    ("ROSE", "Flower with thorns"),
    ("DAISY", "Flower with white petals"),
    ("TULIP", "Flower Holland is famous for"),
    ("SEED", "It grows into a plant"),
    ("GRASS", "Green lawn cover"),
    ("STONE", "Small rock"),
    ("SAND", "Beach ground"),
    ("SHELL", "Beach find with a spiral"),
    ("WAVE", "Surfer's ride"),
    ("POND", "Small water body with lily pads"),
    ("BRIDGE", "It spans a river"),
    ("TOWER", "Tall narrow building"),
    ("CASTLE", "Home with a moat and towers"),
    ("FARM", "Place with barns and tractors"),
    ("ZOO", "Place to see lions and tigers"),
    ("PARK", "Green space with benches"),
    ("CITY", "Big urban area"),
    ("TOWN", "Smaller than a city"),
    ("STORE", "Place to shop"),
    ("MONEY", "Bills and coins"),
    ("COIN", "Penny or nickel"),
    ("GIFT", "Wrapped present"),
    ("PARTY", "Celebration with balloons"),
    ("CANDY", "Sweet Halloween haul"),
    ("COOKIE", "Chocolate chip treat"),
    ("DONUT", "Fried treat with a hole"),
    ("CANDLE", "It's blown out on a birthday cake"),
    ("BELL", "It rings"),
    ("DRESS", "One-piece outfit"),
    ("POCKET", "Pants storage spot"),
    ("BUTTON", "Shirt fastener"),
    ("ZIPPER", "Jacket fastener with teeth"),
    ("LADDER", "Climbing tool with rungs"),
    ("HAMMER", "Nail driver"),
    ("NAIL", "It's hit by a hammer"),
    ("ROPE", "Thick cord for climbing"),
    ("KEY", "It opens a lock"),
    ("LOCK", "A key opens it"),
    ("BOX", "Cardboard container"),
    ("BAG", "Grocery carrier"),
    ("CUP", "Coffee holder"),
    ("PLATE", "Dinner is served on it"),
    ("FORK", "Utensil with prongs"),
    ("SPOON", "Soup utensil"),
    ("KNIFE", "Cutting utensil"),
    ("POT", "Cooking vessel for soup"),
    ("PAN", "Frying vessel"),
    ("OVEN", "Where cookies bake"),
    ("SINK", "Where dishes get washed"),
    ("SOAP", "Bath-time bubbles source"),
    ("TOWEL", "Post-shower dryer"),
    ("MIRROR", "It shows your reflection"),
    ("ICE", "Frozen water"),
    ("STEAM", "What a kettle puffs out"),
    ("NIGHT", "Opposite of day"),
    ("NOON", "Twelve o'clock in the day"),
    ("WEEK", "Seven days"),
    ("YEAR", "Twelve months"),
    ("APRIL", "Month known for showers"),
    ("JULY", "Month of American fireworks"),
    ("FRIEND", "Pal or buddy"),
    ("FAMILY", "Parents and kids together"),
    ("BABY", "Newborn"),
    ("TWIN", "One of two lookalikes"),
    ("UNCLE", "Your parent's brother"),
    ("AUNT", "Your parent's sister"),
    ("HERO", "Person who saves the day"),
    ("JOKE", "It ends with a punchline"),
    ("RIDDLE", "Brain-teasing question"),
    ("SECRET", "Something kept hidden"),
    ("LUCK", "A four-leaf clover brings it"),
    ("WISH", "What you make on a shooting star"),
]

MEDIUM = [
    ("GALAXY", "The Milky Way is one"),
    ("NEBULA", "Colorful cloud of space gas"),
    ("ORBIT", "Path of a planet around the sun"),
    ("ECLIPSE", "When the moon blocks the sun"),
    ("JUPITER", "Largest planet in our solar system"),
    ("SATURN", "Planet famous for its rings"),
    ("MERCURY", "Planet closest to the sun, or a liquid metal"),
    ("NEPTUNE", "Blue planet farthest from the sun"),
    ("METEOR", "Shooting star, really"),
    ("GRAVITY", "Force that keeps you grounded"),
    ("ATOM", "Smallest unit of an element"),
    ("NEUTRON", "Chargeless particle in an atom"),
    ("OXYGEN", "Gas we breathe to live"),
    ("HELIUM", "Gas that makes balloons float"),
    ("CARBON", "Element in diamonds and pencils"),
    ("FOSSIL", "Dinosaur remains in rock"),
    ("VOLCANO", "Mountain that erupts"),
    ("LAVA", "Molten rock above ground"),
    ("MAGMA", "Molten rock below ground"),
    ("GLACIER", "Slow-moving river of ice"),
    ("TSUNAMI", "Giant ocean wave"),
    ("TORNADO", "Twisting funnel of wind"),
    ("MONSOON", "Seasonal drenching rains of Asia"),
    ("EQUATOR", "Imaginary line around Earth's middle"),
    ("COMPASS", "Tool that points north"),
    ("LATITUDE", "Distance north or south of the equator"),
    ("PENGUIN", "Tuxedoed bird that can't fly"),
    ("OSTRICH", "Largest living bird"),
    ("FLAMINGO", "Pink bird that stands on one leg"),
    ("PELICAN", "Bird with a pouched bill"),
    ("TOUCAN", "Rainforest bird with a huge colorful beak"),
    ("FALCON", "Fastest bird in a dive"),
    ("CONDOR", "Huge vulture of the Andes"),
    ("OCTOPUS", "Eight-armed sea creature"),
    ("DOLPHIN", "Clever marine mammal"),
    ("NARWHAL", "Whale with a unicorn-like tusk"),
    ("JELLYFISH", "Stinging sea drifter"),
    ("LOBSTER", "Clawed shellfish delicacy"),
    ("STINGRAY", "Flat fish with a whiplike tail"),
    ("SEAHORSE", "Fish whose males carry the babies"),
    ("GIRAFFE", "Tallest land animal"),
    ("CHEETAH", "Fastest land animal"),
    ("LEOPARD", "Spotted big cat"),
    ("GORILLA", "Largest of the great apes"),
    ("BABOON", "Monkey with a colorful behind"),
    ("HYENA", "African animal with a laughing call"),
    ("MEERKAT", "Upright-standing mongoose of the Kalahari"),
    ("BUFFALO", "Bison's nickname"),
    ("ANTELOPE", "Swift horned grazer of the savanna"),
    ("PANTHER", "Black big cat"),
    ("RACCOON", "Masked trash-can bandit"),
    ("OPOSSUM", "Marsupial that plays dead"),
    ("BEAVER", "Dam-building rodent"),
    ("BADGER", "Burrowing black-and-white mammal"),
    ("HEDGEHOG", "Small spiny mammal that rolls up"),
    ("PLATYPUS", "Egg-laying mammal with a bill"),
    ("KOALA", "Eucalyptus-eating Aussie animal"),
    ("WOMBAT", "Burrowing Australian marsupial"),
    ("IGUANA", "Large tropical lizard"),
    ("GECKO", "Lizard that walks up walls"),
    ("PYTHON", "Huge constricting snake, or a coding language"),
    ("COBRA", "Snake with a hood"),
    ("TORTOISE", "Slow land turtle in a famous fable"),
    ("SCORPION", "Arachnid with a stinging tail"),
    ("TARANTULA", "Big hairy spider"),
    ("MOSQUITO", "Buzzing summer biter"),
    ("CRICKET", "Chirping insect, or a bat-and-ball sport"),
    ("BEETLE", "Insect with hard wing covers, or a VW car"),
    ("CATERPILLAR", "It becomes a butterfly"),
    ("CHRYSALIS", "Butterfly's transformation case"),
    ("AVOCADO", "Green fruit in guacamole"),
    ("BROCCOLI", "Green vegetable like little trees"),
    ("SPINACH", "Leafy green that made Popeye strong"),
    ("EGGPLANT", "Purple vegetable in ratatouille"),
    ("ZUCCHINI", "Green summer squash"),
    ("PUMPKIN", "Jack-o'-lantern squash"),
    ("COCONUT", "Hairy tropical fruit with milk inside"),
    ("PINEAPPLE", "Spiky tropical fruit"),
    ("PAPAYA", "Orange tropical fruit with black seeds"),
    ("APRICOT", "Small orange stone fruit"),
    ("RHUBARB", "Tart red stalk baked into pies"),
    ("LASAGNA", "Layered Italian pasta dish"),
    ("RAVIOLI", "Stuffed pasta pillows"),
    ("GNOCCHI", "Italian potato dumplings"),
    ("RISOTTO", "Creamy Italian rice dish"),
    ("PAELLA", "Spanish saffron rice dish"),
    ("BURRITO", "Big wrapped Mexican meal"),
    ("GUACAMOLE", "Avocado dip"),
    ("HUMMUS", "Chickpea dip"),
    ("FALAFEL", "Fried chickpea balls"),
    ("SUSHI", "Japanese rice-and-fish rolls"),
    ("WASABI", "Fiery green sushi paste"),
    ("TERIYAKI", "Sweet Japanese glaze"),
    ("CROISSANT", "Flaky French crescent pastry"),
    ("BAGUETTE", "Long French loaf"),
    ("ECLAIR", "Cream-filled French pastry"),
    ("MACARON", "Colorful French sandwich cookie"),
    ("TIRAMISU", "Coffee-soaked Italian dessert"),
    ("PRETZEL", "Twisted salty snack"),
    ("WAFFLE", "Breakfast food with a grid pattern"),
    ("OMELET", "Folded egg dish"),
    ("ESPRESSO", "Strong little coffee"),
    ("CINNAMON", "Spice in snickerdoodles"),
    ("VANILLA", "Classic ice cream flavor from an orchid"),
    ("CARAMEL", "Chewy golden candy"),
    ("LICORICE", "Black rope candy"),
    ("MARZIPAN", "Almond confection"),
    ("VENICE", "Italian city of canals and gondolas"),
    ("ATHENS", "City of the Parthenon"),
    ("VIENNA", "Waltzing capital of Austria"),
    ("LISBON", "Capital of Portugal"),
    ("DUBLIN", "Capital of Ireland"),
    ("MOSCOW", "City of the Kremlin"),
    ("BEIJING", "Capital of China"),
    ("NAIROBI", "Capital of Kenya"),
    ("HAVANA", "Cuban capital of classic cars"),
    ("TORONTO", "Canadian city with the CN Tower"),
    ("CHICAGO", "The Windy City"),
    ("SEATTLE", "Rainy city with the Space Needle"),
    ("DENVER", "The Mile High City"),
    ("ARIZONA", "Grand Canyon State"),
    ("VERMONT", "Maple syrup state"),
    ("FLORIDA", "The Sunshine State"),
    ("MONTANA", "Big Sky Country"),
    ("NEVADA", "Las Vegas's state"),
    ("BRAZIL", "Home of Rio's Carnival"),
    ("MOROCCO", "North African land of Casablanca"),
    ("ICELAND", "Island nation of geysers"),
    ("NORWAY", "Land of fjords"),
    ("SAHARA", "World's largest hot desert"),
    ("AMAZON", "World's largest rainforest"),
    ("EVEREST", "World's highest peak"),
    ("ATLANTIS", "Legendary sunken city"),
    ("PYRAMID", "Pharaoh's pointed tomb"),
    ("SPHINX", "Egyptian statue with a riddle-loving cousin"),
    ("PHARAOH", "Ancient Egyptian ruler"),
    ("GLADIATOR", "Fighter in the Colosseum"),
    ("SAMURAI", "Sword-wielding Japanese warrior"),
    ("VIKING", "Norse seafaring raider"),
    ("PEGASUS", "Winged horse of myth"),
    ("PHOENIX", "Bird reborn from its ashes"),
    ("MEDUSA", "Gorgon with snakes for hair"),
    ("KRAKEN", "Legendary giant sea monster"),
    ("CENTAUR", "Half man, half horse"),
    ("UNICORN", "One-horned mythical horse"),
    ("MERMAID", "Half woman, half fish"),
    ("ZOMBIE", "Shuffling movie undead"),
    ("VAMPIRE", "Count Dracula, for one"),
    ("MUMMY", "Bandage-wrapped monster"),
    ("GOBLIN", "Mischievous fantasy creature"),
    ("TROLL", "Bridge-guarding brute of folklore"),
    ("EXCALIBUR", "King Arthur's sword"),
    ("CAMELOT", "King Arthur's castle"),
    ("ODYSSEY", "Homer's epic voyage"),
    ("TRIDENT", "Poseidon's three-pronged spear"),
    ("OLYMPUS", "Mountain home of Greek gods"),
    ("MARATHON", "26.2-mile race"),
    ("JAVELIN", "Spear thrown at track meets"),
    ("BIATHLON", "Skiing-and-shooting sport"),
    ("ARCHERY", "Sport of bows and arrows"),
    ("FENCING", "Sword-fighting sport"),
    ("KARATE", "Japanese martial art"),
    ("JUDO", "Martial art of throws"),
    ("SLALOM", "Zigzag ski race"),
    ("REGATTA", "Boat race series"),
    ("STADIUM", "Big sports arena"),
    ("TROPHY", "Champion's prize cup"),
    ("REFEREE", "Official with a whistle"),
    ("PENALTY", "Foul's consequence"),
    ("OVERTIME", "Extra period to break a tie"),
    ("HOMERUN", "Baseball hit clear out of the park"),
    ("STRIKEOUT", "Pitcher's three-strike triumph"),
    ("TOUCHDOWN", "Six points in football"),
    ("BIRDIE", "One under par in golf"),
    ("CADDIE", "Golfer's club carrier"),
    ("GUITAR", "Six-stringed instrument"),
    ("UKULELE", "Small Hawaiian strummer"),
    ("BANJO", "Twangy bluegrass instrument"),
    ("CELLO", "Deep-voiced string instrument"),
    ("TRUMPET", "Brass horn with three valves"),
    ("TROMBONE", "Brass instrument with a slide"),
    ("SAXOPHONE", "Jazzy reed instrument"),
    ("ACCORDION", "Squeezebox instrument"),
    ("ORCHESTRA", "Large group of musicians"),
    ("MAESTRO", "Distinguished conductor"),
    ("SOPRANO", "Highest singing voice"),
    ("FALSETTO", "Artificially high singing voice"),
    ("MELODY", "The tune you hum"),
    ("RHYTHM", "The beat of a song"),
    ("ENCORE", "Crowd's request for one more song"),
    ("KARAOKE", "Sing-along with a lyric screen"),
    ("BALLET", "Dance with tutus and pointe shoes"),
    ("TANGO", "Dramatic dance from Argentina"),
    ("POLKA", "Lively dance, or a dot pattern"),
    ("WALTZ", "Dance in three-four time"),
    ("THEATER", "Where plays are staged"),
    ("MATINEE", "Afternoon showing"),
    ("SEQUEL", "The movie that comes after"),
    ("VILLAIN", "Story's bad guy"),
    ("CLIMAX", "Story's most exciting point"),
    ("NARRATOR", "Voice telling the story"),
    ("MYSTERY", "Whodunit genre"),
    ("WESTERN", "Cowboy movie genre"),
    ("DIRECTOR", "One who yells 'Action!'"),
    ("SCRIPT", "Actor's lines, collectively"),
    ("COSTUME", "Actor's outfit"),
    ("PREMIERE", "Film's first showing"),
    ("CARTOON", "Animated show"),
    ("ORIGAMI", "Japanese paper folding"),
    ("MOSAIC", "Art made of tiny tiles"),
    ("PORTRAIT", "Painting of a person"),
    ("GALLERY", "Room where art hangs"),
    ("SCULPTOR", "Artist who works in marble"),
    ("CHARCOAL", "Sketcher's black stick"),
    ("EASEL", "Painter's canvas stand"),
    ("PALETTE", "Painter's mixing board"),
    ("CANVAS", "Painter's fabric surface"),
    ("ANAGRAM", "Word made by scrambling another"),
    ("ACRONYM", "NASA or LOL, e.g."),
    ("PROVERB", "Wise old saying"),
    ("METAPHOR", "Comparison without 'like' or 'as'"),
    ("HAIKU", "Seventeen-syllable poem"),
    ("SONNET", "Fourteen-line poem"),
    ("LIBRARY", "Building full of books"),
    ("ALMANAC", "Yearly book of facts"),
    ("ATLAS", "Book of maps"),
    ("GLOSSARY", "Book's list of term definitions"),
    ("JOURNAL", "Daily diary"),
    ("POSTCARD", "Vacation greeting in the mail"),
    ("ENVELOPE", "A letter travels in it"),
    ("TELEGRAM", "Old-time wired message"),
    ("ANTENNA", "Signal catcher on a roof, or a bug's feeler"),
    ("SATELLITE", "Orbiting signal relay"),
    ("KEYBOARD", "Typist's rows of keys"),
    ("BROWSER", "App for surfing the web"),
    ("PIXEL", "Tiniest dot on a screen"),
    ("PODCAST", "Downloadable talk show"),
    ("EMOJI", "Tiny picture in a text message"),
    ("AVATAR", "Your on-screen persona"),
    ("GADGET", "Handy little device"),
    ("TURBINE", "Spinning power generator"),
    ("PENDULUM", "Grandfather clock's swinger"),
    ("SUNDIAL", "Shadow-casting timekeeper"),
    ("HOURGLASS", "Sand-filled timer"),
    ("COMPOST", "Gardener's recycled scraps"),
    ("ORCHID", "Exotic showy flower"),
    ("BONSAI", "Miniature sculpted tree"),
    ("CACTUS", "Prickly desert plant"),
    ("BAMBOO", "Panda's favorite plant"),
    ("SEQUOIA", "Giant California tree"),
    ("ACORN", "Oak tree's nut"),
    ("POLLEN", "Sneeze-inducing flower dust"),
    ("HARVEST", "Autumn crop gathering"),
    ("ORCHARD", "Field of fruit trees"),
    ("VINEYARD", "Where wine grapes grow"),
    ("SCARECROW", "Field guardian stuffed with straw"),
    ("LANTERN", "Portable light with a handle"),
    ("HAMMOCK", "Hanging bed between trees"),
    ("BONFIRE", "Big outdoor blaze"),
    ("CAMPSITE", "Where tents get pitched"),
    ("BACKPACK", "Hiker's gear carrier"),
    ("BINOCULARS", "Birdwatcher's two-eyed lenses"),
    ("SOUVENIR", "Trip keepsake"),
    ("PASSPORT", "Traveler's ID booklet"),
    ("LUGGAGE", "Traveler's bags"),
    ("VOYAGE", "Long journey by sea"),
    ("CARAVAN", "Group traveling together"),
    ("GONDOLA", "Venetian canal boat"),
    ("SUBMARINE", "Underwater vessel"),
    ("ZEPPELIN", "Rigid airship"),
    ("MONORAIL", "Single-track train"),
    ("RICKSHAW", "Pulled two-wheeled taxi"),
    ("LIGHTHOUSE", "Coastal beacon tower"),
    ("HARBOR", "Safe place for ships"),
    ("ANCHOR", "It keeps a ship in place"),
    ("COMPASS", "Navigator's direction finder"),
    ("TREASURE", "What X marks on a pirate map"),
    ("GALLEON", "Big old Spanish sailing ship"),
    ("CUTLASS", "Pirate's curved sword"),
    ("PARROT", "Pirate's talkative shoulder pet"),
    ("AVALANCHE", "Sudden mountain snowslide"),
    ("BLIZZARD", "Blinding snowstorm"),
    ("HUMIDITY", "Mugginess in the air"),
    ("FORECAST", "Meteorologist's prediction"),
    ("RAINBOW", "Arc after a storm"),
    ("HORIZON", "Where sky meets earth"),
    ("TWILIGHT", "Dim time after sunset"),
    ("MIDNIGHT", "Twelve o'clock at night"),
    ("SOLSTICE", "Longest or shortest day"),
    ("CALENDAR", "Wall chart of months"),
    ("ANTIDOTE", "Poison's counteragent"),
    ("BANDAGE", "Wound wrap"),
    ("VACCINE", "Preventive shot"),
    ("STETHOSCOPE", "Doctor's listening tool"),
    ("SKELETON", "Your 206 bones, collectively"),
    ("CRANIUM", "Skull's brain case"),
    ("MUSCLE", "Bicep or tricep"),
    ("APPETITE", "Desire for food"),
    ("YAWN", "Sleepy mouth stretch"),
    ("HICCUP", "Involuntary 'hic!'"),
    ("WHISPER", "Very quiet speech"),
    ("APPLAUSE", "Sound of many clapping hands"),
    ("CHUCKLE", "Quiet little laugh"),
    ("GIGGLE", "Schoolkid's laugh"),
    ("GRIMACE", "Face of disgust"),
    ("SHIVER", "Cold-weather tremble"),
    ("CURIOUS", "Eager to find out"),
    ("JUBILANT", "Overjoyed"),
    ("SERENE", "Calm and peaceful"),
    ("FRUGAL", "Careful with money"),
    ("NIMBLE", "Quick and light on one's feet"),
    ("STUBBORN", "Mule-like in attitude"),
    ("HUMBLE", "Not boastful"),
    ("VALIANT", "Brave and heroic"),
    ("DAZZLE", "Impress brilliantly"),
    ("MEANDER", "Wander like a lazy river"),
    ("PONDER", "Think deeply"),
    ("SCRIBBLE", "Write messily"),
    ("JUGGLE", "Keep three balls in the air"),
    ("WHITTLE", "Carve wood bit by bit"),
    ("RUMMAGE", "Dig through a drawer"),
    ("BARTER", "Trade without money"),
    ("AUCTION", "Sale to the highest bidder"),
    ("BAZAAR", "Bustling market"),
    ("BOUTIQUE", "Small fashionable shop"),
    ("EMPORIUM", "Grand store of many goods"),
    ("HEIRLOOM", "Treasure passed down in a family"),
    ("ANTIQUE", "Valuable old object"),
    ("LOCKET", "Necklace that holds a tiny photo"),
    ("EMERALD", "Green gemstone"),
    ("SAPPHIRE", "Blue gemstone"),
    ("OPAL", "Iridescent October birthstone"),
    ("TOPAZ", "November's golden birthstone"),
    ("GRANITE", "Speckled countertop stone"),
    ("MARBLE", "Sculptor's white stone, or a small glass ball"),
    ("QUARTZ", "Common crystal in watches"),
    ("GEYSER", "Old Faithful, for one"),
    ("CANYON", "Deep river-carved gorge"),
    ("PLATEAU", "High flat landform"),
    ("LAGOON", "Calm pool by the sea"),
    ("ARCHIPELAGO", "Chain of islands"),
    ("PENINSULA", "Land jutting into water"),
    ("DELTA", "River's fan-shaped mouth"),
    ("TUNDRA", "Frozen treeless plain"),
    ("SAVANNA", "Grassy plain with scattered trees"),
    ("JUNGLE", "Dense tropical forest"),
    ("BUNGALOW", "Cozy one-story house"),
    ("CHIMNEY", "Santa's entrance"),
    ("VERANDA", "Roofed open porch"),
    ("GAZEBO", "Open garden pavilion"),
    ("TURRET", "Castle's little tower"),
    ("DUNGEON", "Castle's dark prison"),
    ("CATACOMB", "Underground burial tunnel"),
    ("LABYRINTH", "Elaborate maze"),
    ("OBELISK", "Tall four-sided stone pillar"),
    ("AQUEDUCT", "Roman water channel"),
    ("COLOSSEUM", "Rome's great arena"),
    ("PAGODA", "Tiered Asian tower"),
    ("IGLOO", "Dome of snow blocks"),
    ("TEEPEE", "Cone-shaped Plains dwelling"),
    ("HAMLET", "Tiny village, or a Danish prince"),
    ("METROPOLIS", "Huge bustling city"),
    ("CARNIVAL", "Fair with rides and games"),
    ("CAROUSEL", "Merry-go-round"),
    ("FERRIS", "___ wheel, fair's big ride"),
    ("ACROBAT", "Circus tumbler"),
    ("TRAPEZE", "Circus flyer's swinging bar"),
    ("TIGHTROPE", "High wire for a daring walker"),
    ("VENTRILOQUIST", "Performer whose dummy 'talks'"),
    ("CHARADES", "Acting-out guessing game"),
    ("DOMINO", "Dotted tile that topples in chains"),
    ("ROULETTE", "Casino wheel game"),
    ("JACKPOT", "Slot machine's big payout"),
    ("WILDCARD", "It can stand for anything"),
    ("CHECKMATE", "Chess game ender"),
    ("GAMBIT", "Chess opening sacrifice"),
    ("STALEMATE", "Chess draw, or any deadlock"),
    ("SUDOKU", "Number-grid logic puzzle"),
    ("CIPHER", "Secret code"),
    ("ENIGMA", "Baffling mystery"),
    ("ALIBI", "Suspect's 'I was elsewhere' claim"),
    ("SLEUTH", "Detective, informally"),
    ("CULPRIT", "The guilty one"),
    ("VERDICT", "Jury's decision"),
    ("GAVEL", "Judge's hammer"),
    ("INCOGNITO", "In disguise"),
    ("DECOY", "Lure meant to mislead"),
    ("ESPIONAGE", "Spy work"),
    ("SABOTAGE", "Deliberate wrecking"),
    ("AMBUSH", "Surprise attack from hiding"),
    ("FORTRESS", "Stronghold"),
    ("ARMADA", "Great fleet of warships"),
    ("CATAPULT", "Medieval stone flinger"),
    ("CHARIOT", "Two-wheeled ancient racer"),
    ("SCABBARD", "Sword's sheath"),
    ("GAUNTLET", "Armored glove thrown down"),
    ("HERALD", "Royal announcer"),
    ("SCEPTER", "Monarch's ceremonial staff"),
    ("MONARCH", "King or queen, or an orange butterfly"),
    ("DYNASTY", "Line of rulers from one family"),
    ("EMPIRE", "Realm of many nations under one ruler"),
    ("TREATY", "Peace agreement"),
    ("DIPLOMAT", "Embassy negotiator"),
    ("CHANCELLOR", "Germany's head of government"),
    ("BALLOT", "Voter's slip"),
    ("QUORUM", "Minimum members needed to vote"),
    ("VETO", "Presidential rejection"),
]

# ---------------------------------------------------------------------------
# Criss-cross crossword builder
# ---------------------------------------------------------------------------


class Builder:
    def __init__(self, size, rng):
        self.size = size
        self.rng = rng
        self.grid = [[None] * size for _ in range(size)]
        self.placed = []  # (word, row, col, horizontal)

    def cell(self, r, c):
        if 0 <= r < self.size and 0 <= c < self.size:
            return self.grid[r][c]
        return None

    def can_place(self, word, r, c, horiz):
        n = len(word)
        dr, dc = (0, 1) if horiz else (1, 0)
        end_r, end_c = r + dr * (n - 1), c + dc * (n - 1)
        if r < 0 or c < 0 or end_r >= self.size or end_c >= self.size:
            return False
        # cell before start and after end must be empty
        if self.cell(r - dr, c - dc) is not None:
            return False
        if self.cell(end_r + dr, end_c + dc) is not None:
            return False
        crossings = 0
        for i, ch in enumerate(word):
            rr, cc = r + dr * i, c + dc * i
            cur = self.grid[rr][cc]
            if cur is not None:
                if cur != ch:
                    return False
                crossings += 1
            else:
                # sides perpendicular to direction must be empty
                if horiz:
                    if self.cell(rr - 1, cc) is not None or self.cell(rr + 1, cc) is not None:
                        return False
                else:
                    if self.cell(rr, cc - 1) is not None or self.cell(rr, cc + 1) is not None:
                        return False
        if self.placed and crossings == 0:
            return False
        return True

    def place(self, word, r, c, horiz):
        dr, dc = (0, 1) if horiz else (1, 0)
        for i, ch in enumerate(word):
            self.grid[r + dr * i][c + dc * i] = ch
        self.placed.append((word, r, c, horiz))

    def try_add(self, word):
        """Try to place word crossing an existing word; return True on success."""
        options = []
        for pw, pr, pc, ph in self.placed:
            pdr, pdc = (0, 1) if ph else (1, 0)
            for j, pch in enumerate(pw):
                for i, ch in enumerate(word):
                    if ch != pch:
                        continue
                    cr, cc = pr + pdr * j, pc + pdc * j
                    if ph:  # place new word vertically through (cr, cc)
                        nr, nc, nh = cr - i, cc, False
                    else:
                        nr, nc, nh = cr, cc - i, True
                    if self.can_place(word, nr, nc, nh):
                        options.append((nr, nc, nh))
        if not options:
            return False
        nr, nc, nh = self.rng.choice(options)
        self.place(word, nr, nc, nh)
        return True


def build_puzzle(bank, size, min_words, max_words, rng):
    words = bank[:]
    rng.shuffle(words)
    b = Builder(size, rng)
    # seed with a longish word placed horizontally near the center
    seed_pool = [w for w in words if len(w[0]) >= min(6, size - 3)] or words
    seed = rng.choice(seed_pool[:30])
    r = size // 2
    c = (size - len(seed[0])) // 2
    b.place(seed[0], r, c, True)
    used = {seed[0]: seed[1]}
    for _sweep in range(3):
        if len(b.placed) >= max_words:
            break
        for w, clue in words:
            if w in used or len(w) > size:
                continue
            if b.try_add(w):
                used[w] = clue
                if len(b.placed) >= max_words:
                    break
    if len(b.placed) < min_words:
        return None
    return finalize(b, used)


def finalize(b, used):
    # bounding box + center the grid
    rows = [r for r in range(b.size) for c in range(b.size) if b.grid[r][c]]
    cols = [c for r in range(b.size) for c in range(b.size) if b.grid[r][c]]
    r0, r1, c0, c1 = min(rows), max(rows), min(cols), max(cols)
    h, w = r1 - r0 + 1, c1 - c0 + 1
    size = max(h, w)
    off_r = (size - h) // 2 - r0
    off_c = (size - w) // 2 - c0
    grid = [[None] * size for _ in range(size)]
    for r in range(b.size):
        for c in range(b.size):
            if b.grid[r][c]:
                grid[r + off_r][c + off_c] = b.grid[r][c]

    # standard numbering
    def starts_across(r, c):
        if grid[r][c] is None:
            return False
        left = grid[r][c - 1] if c > 0 else None
        right = grid[r][c + 1] if c + 1 < size else None
        return left is None and right is not None

    def starts_down(r, c):
        if grid[r][c] is None:
            return False
        up = grid[r - 1][c] if r > 0 else None
        down = grid[r + 1][c] if r + 1 < size else None
        return up is None and down is not None

    clue_by_word = dict(used)
    across, down = [], []
    num = 0
    for r in range(size):
        for c in range(size):
            sa, sd = starts_across(r, c), starts_down(r, c)
            if not (sa or sd):
                continue
            num += 1
            if sa:
                cc = c
                letters = []
                while cc < size and grid[r][cc] is not None:
                    letters.append(grid[r][cc])
                    cc += 1
                word = "".join(letters)
                across.append([num, r, c, len(word), clue_by_word[word]])
            if sd:
                rr = r
                letters = []
                while rr < size and grid[rr][c] is not None:
                    letters.append(grid[rr][c])
                    rr += 1
                word = "".join(letters)
                down.append([num, r, c, len(word), clue_by_word[word]])

    g = ["".join(ch if ch else "." for ch in row) for row in grid]
    return {"s": size, "g": g, "a": across, "d": down,
            "words": frozenset(clue_by_word)}


def verify(p):
    """Sanity checks: every across/down run has a clue entry, grid connected."""
    size, g = p["s"], p["g"]
    entries = len(p["a"]) + len(p["d"])
    assert entries >= 6, "too few entries"
    # connectivity of filled cells
    cells = {(r, c) for r in range(size) for c in range(size) if g[r][c] != "."}
    assert cells
    stack = [next(iter(cells))]
    seen = set(stack)
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if (nr, nc) in cells and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    assert seen == cells, "grid not connected"
    # every clue matches grid letters and lengths, no 1-letter runs unclued
    for lst, horiz in ((p["a"], True), (p["d"], False)):
        for num, r, c, ln, clue in lst:
            assert ln >= 2
            for i in range(ln):
                rr, cc = (r, c + i) if horiz else (r + i, c)
                assert g[rr][cc] != "."


def make_set(bank, count, size, min_words, max_words, seed):
    rng = random.Random(seed)
    puzzles, sigs = [], set()
    attempts = 0
    while len(puzzles) < count:
        attempts += 1
        if attempts > count * 400:
            raise RuntimeError("could not generate enough distinct puzzles")
        p = build_puzzle(bank, size, min_words, max_words, rng)
        if p is None or p["words"] in sigs:
            continue
        verify(p)
        sigs.add(p["words"])
        del p["words"]
        puzzles.append(p)
    return puzzles


def main():
    easy = make_set(EASY, 100, size=9, min_words=9, max_words=11, seed=20260901)
    medium = make_set(MEDIUM, 100, size=13, min_words=12, max_words=15, seed=90210)
    data = {"easy": easy, "medium": medium}
    out = "window.PUZZLES = " + json.dumps(data, separators=(",", ":")) + ";\n"
    path = sys.argv[1] if len(sys.argv) > 1 else "puzzles.js"
    with open(path, "w") as f:
        f.write(out)
    ecount = sum(len(p["a"]) + len(p["d"]) for p in easy) / len(easy)
    mcount = sum(len(p["a"]) + len(p["d"]) for p in medium) / len(medium)
    print(f"easy: {len(easy)} puzzles, avg {ecount:.1f} entries")
    print(f"medium: {len(medium)} puzzles, avg {mcount:.1f} entries")
    print(f"wrote {path} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
