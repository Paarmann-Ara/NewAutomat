from data_structure.data_structure_provider import DataStructureProvider

DataStructure_dictionary = DataStructureProvider().dictionary_manager_class

added, removed, difference, commen = DataStructure_dictionary.compair({'f':'f','j':'j'},{'f':'f1', 'k':'k'})

print(added, removed, difference, commen)