using Microsoft.EntityFrameworkCore;
using MVC2.Models;

namespace MVC2.Data
{
	public class ApplicationDbContext : DbContext
	{
        public DbSet<Employee> Employees{ get; set; }

        public ApplicationDbContext(DbContextOptions options):base(options)
        {
                
        }
    }
}
