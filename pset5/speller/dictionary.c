/**
 * Implements a dictionary's functionality.
 */

#include "dictionary.h"

// initiate a global hashtable, one linked list for each letter
node *dict_hash[26];

// initiate a global size counter
int dict_size = 0;

// hash function
int hash(char *item)
{
    // return the ASCII code for lowercase letters as hashtable indexes, offset to start at 0
    if (isalpha(item[0]))
    {
        int index = ((int)tolower(item[0])) - 97;
        return index;        
    }
    else
    {
        return 0;
    }
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // allocate memory to each linked list header in the hashtable
    for (int i = 0; i < 26; i++)
    {
        dict_hash[i] = malloc(sizeof(node));
    }
    
    // scan dictionary file item by item
    FILE *dict_file = fopen(dictionary, "r");
    char dict_item[LENGTH + 1];
    while (fscanf(dict_file, "%s", dict_item) != EOF)
    {
        // create a new dictionary node
        node *dict_node = malloc(sizeof(node));
        if (dict_node == NULL)
        {
            unload();
            return false;
        }
        // copy dictionary item to node
        strcpy(dict_node->word, dict_item);
        // increase dictionary size by 1
        dict_size += 1;
        // obtain appropriate hash index for the node
        int dict_index = hash(dict_node->word);
        // insert node to the appropriate linked list
        dict_node->next = dict_hash[dict_index]->next;
        dict_hash[dict_index]->next = dict_node;
    }
    
    // load success
    fclose(dict_file);
    return true;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // generate a non-constant copy of word
    char check_word[LENGTH + 1];
    strcpy(check_word, word);
    // initiate a check cursor pointing at the appropriate linked list
    node *check_cursor = dict_hash[hash(check_word)];
    if (check_cursor == NULL)
    {
        unload();
        return false;
    }
    // compare word to one dictionary node at a time 
    while (check_cursor != NULL)
    {
        if (strcasecmp(check_word, check_cursor->word) == 0)
        {
            return true;
        }
        check_cursor = check_cursor->next;
    }
    
    // exit function
    return false;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (dict_size == 0)
    {
        return 0;
    }
    return dict_size;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i < 26; i++)
    {
        // initiate unload cursor at each linked list
        node *unload_cursor = dict_hash[i];
        
        // unload one node at a time for each linked list
        while (unload_cursor != NULL)
        {
            node *current_node = unload_cursor;
            unload_cursor = unload_cursor->next;
            free(current_node);
        }        
    }
    
    // unload success
    return true;
}
