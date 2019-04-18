
job = 35

filename = "job{0}_{1}_completed_accessURLs.txt".format(job,jobs(35).name)
print ("Writing accessURLs to {0}".format(filename))

f = open(filename, "w")
for job in jobs(35).subjobs.select(status='completed') :
  files = job.backend.getOutputDataAccessURLs()
  thefile = files[0]
  print(thefile)
  f.write(thefile + "\n")

f.close()

