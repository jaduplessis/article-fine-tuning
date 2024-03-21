

base_message = """
I am preparing documents to provide to an LLM to fine tune it.  You are a text neutraliser. Your task is to take stylistic or expressive text as input and convert it into a neutral, concise and plain version while preserving the core meaning and factual information.

Constraint: The neutral text output should be in regular text format, NOT in HTML or markdown. If any code snippets are encountered, leave them exactly as they are. Only return the transformed text. DO NOT include any reference to the request itself.
ONLY transform the text. Do not add any additional information or comments. DO NOT PROVIDE anything like "Neutral text:" or "<your neutral text>".
"""


style_variation = {
  "draft": """
  Style: Vary the original vocabulary, tone and prose.  The style should revert back to the initial draft format of a writing plan. It should be a framework outlining the main ideas and paragraph planning that is expected in the initial stages of writing. Use a concise bullet point formatting

  Here is an example of the original text and the neutralised version.

  Example 1: 
  User Input
  ========
  <h1>Understanding Eventual Consistency in DynamoDB</h1><p>One of the core complaints I hear about DynamoDB is that it can't be used for critical applications because it only provides eventual consistency.</p><p>It's true that eventual consistency can add complications to your application, but I've found these problems can be handled in most situations. Further, even your "strongly consistent" relational databases can result in issues if you're not careful about isolation or your choice of ORM. Finally, the benefits from accepting a bit of eventual consistency can be pretty big.</p><p>In this post, I want to dispel some of the fear around eventual consistency in DynamoDB.</p><p>We'll walk through this in three different sections:</p><p>My hope is that you can use this to make a more informed decision about when and how you can handle eventual consistency in your application.</p>


  Assistant
  =======
  - DynamoDB's eventual consistency model is a common criticism, with concerns about its use in critical applications.
  - Eventual consistency can introduce complications, but these can be managed in most cases.
  - Even strongly consistent relational databases can have issues related to isolation or ORM choices.
  - The benefits of accepting some eventual consistency in DynamoDB can be significant.
  - The post aims to address concerns around eventual consistency in DynamoDB.
  - The content will be covered in three sections.


Example 2:
  User Input
  ========
  <p>For the rest of the item, however, the shape is irrelevant. You won't have foreign key references to other tables, like you would in a relational database. Nor will you have neatly structured result sets with typed columns. Because the primary key is the only thing that matters, the rest of the data is just coming along for the ride.</p><p>DynamoDB is more like a key-value store than a spreadsheet. The key might be simple, with just a partition key, or complex, with a partition key plus a sort key, but the value is still just a blob.</p><p>One word of caution -- DynamoDB's schemaless nature does not mean your data shouldn't have a schema somewhere. You need to maintain and validate your data schemas within your application code rather than relying on your database to handle it.</p>


  Assistant
  =======
  - In DynamoDB, the shape of the item (beyond the primary key) is not important.
  - There are no foreign key references to other tables like in relational databases.
  - Result sets are not neatly structured with typed columns.
  - The primary key is the only significant part, with the rest of the data just accompanying it.
  - DynamoDB is more akin to a key-value store than a spreadsheet.
  - The key can be simple (just a partition key) or complex (partition key plus sort key), but the value is still a blob.
  - DynamoDB's schemaless nature does not mean data should lack a schema - it must be maintained and validated within the application code.
  """,
  "formal": """
  STYLE: Vary the original vocabulary, tone and prose. Make it read more like a dull university essay. I want to be bored by the end of it.
  
  Here is an example of the original text and the neutralised version.

  Example:
  User Input
  ========
  <p>In this post, we'll take a deep look at DynamoDB partitions -- what they are, why they matter, and how they should affect your data modeling. The most important reason to learn about DynamoDB partitions is because it will shape your understanding of why DynamoDB acts as it does. At first glance, the DynamoDB API feels unnecessarily restrictive and the principles of single-table design seem bizarre. Once you understand DynamoDB partitions, you'll see why these things are necessary.</p><p>If you want to skip to specific sections, this post covers:</p><p>Let's get started!</p>


  Assistant
  =======
  
  """,
}

