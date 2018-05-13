# Breadth-first approach
1. Initially all the links from the seed satisfying the given condition(keyword=solar) are traversed and added to the be crawled list.   
2. All these links are at the same level. Then, the first link(which now becomes the seed) from the seed is crawled. All the hyperlinks from this seed are added to the to be crawled list. Then, the second hyperlink from the initial seed becomes seed and all the links from that page are added.  
3. Step 2 continues till the number of crawled hyperlinks is 1000 or the maximum depth is 5, 1 being the depth of the initial seed.  

# Depth-first approach
1. The hyperlinks satisfying the given condition, from the seed are added to the to be crawled list.   
2. The first hyperlink (now: seed and increment depth) from the page is crawled. Then, the first hyperlink (now: seed and increment depth) from this seed is crawled.   
3. Step 2 continues till the depth is 5. After the depth is 5, it crawls the next hyperlink from the list.   
4. Each time if there is a new hyperlink from the seed, it gets added to the start of the list. This process continues till the number of crawled hyperlinks is 1000 or the to be crawled list is empty.  

